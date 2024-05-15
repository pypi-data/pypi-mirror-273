from typing import Optional
import os
import yaml
import time
from pathlib import Path
import shutil
import multiprocessing
from ..common._api_request import _compute_resource_get_api_request
from .register_compute_resource import env_var_keys
from ..common.dendro_types import DendroJob
from ..mock import using_mock
from .AppManager import AppManager
from .JobManager import JobManager


class Daemon:
    def __init__(self):
        self._compute_resource_id = os.getenv('COMPUTE_RESOURCE_ID', None)
        self._compute_resource_private_key = os.getenv('COMPUTE_RESOURCE_PRIVATE_KEY', None)
        if self._compute_resource_id is None:
            raise ValueError('Compute resource has not been initialized in this directory, and the environment variable COMPUTE_RESOURCE_ID is not set.')
        if self._compute_resource_private_key is None:
            raise ValueError('Compute resource has not been initialized in this directory, and the environment variable COMPUTE_RESOURCE_PRIVATE_KEY is not set.')

        available_job_run_methods_str = os.getenv('AVAILABLE_JOB_RUN_METHODS', 'local')
        available_job_run_methods = [s.strip() for s in available_job_run_methods_str.split(',') if s]
        for a in available_job_run_methods:
            if a not in ['local', 'aws_batch', 'slurm']:
                raise ValueError(f'Invalid job run method: {a}')

        self._app_manager = AppManager(
            compute_resource_id=self._compute_resource_id,
            compute_resource_private_key=self._compute_resource_private_key,
            available_job_run_methods=available_job_run_methods # type: ignore
        )
        self._app_manager.update_apps()

        self._job_manager = JobManager(
            compute_resource_id=self._compute_resource_id,
            compute_resource_private_key=self._compute_resource_private_key,
            app_manager=self._app_manager
        )

    def start(self, *, timeout: Optional[float] = None, cleanup_old_jobs=True): # timeout is used for testing
        timer_handle_jobs = 0

        time_scale_factor = 1 if not using_mock() else 10000

        assert self._compute_resource_id is not None
        assert self._compute_resource_private_key is not None

        print('Getting pubsub info')
        pubsub_subscription = get_pubsub_subscription(
            compute_resource_id=self._compute_resource_id,
            compute_resource_private_key=self._compute_resource_private_key
        )
        pubnub_subscribe_key = pubsub_subscription['pubnubSubscribeKey']
        if pubnub_subscribe_key != 'mock-subscribe-key':
            from .PubsubClient import PubsubClient
            pubsub_client = PubsubClient(
                pubnub_subscribe_key=pubnub_subscribe_key,
                pubnub_channel=pubsub_subscription['pubnubChannel'],
                pubnub_user=pubsub_subscription['pubnubUser'],
                compute_resource_id=self._compute_resource_id
            )
        else:
            pubsub_client = None

        # Create file cache directory if needed
        file_cache_dir = os.path.join(os.getcwd(), 'file_cache')
        if not os.path.exists(file_cache_dir):
            os.makedirs(file_cache_dir)

        # Start cleaning up old job directories
        # It's important to do this in a separate process
        # because it can take a long time to delete all the files in the tmp directories (remfile is the culprit)
        # and we don't want to block the main process from handling jobs
        if cleanup_old_jobs:
            cleanup_old_jobs_process = multiprocessing.Process(target=_cleanup_old_job_working_directories, args=(os.getcwd() + '/jobs',))
            cleanup_old_jobs_process.start()
        else:
            cleanup_old_jobs_process = None

        try:
            print('Starting compute resource')
            reported_that_compute_resource_is_running = False
            overall_timer = time.time()
            while True:
                elapsed_handle_jobs = time.time() - timer_handle_jobs
                # normally we will get pubsub messages for updates, but if we don't, we should check every 10 minutes
                time_to_handle_jobs = elapsed_handle_jobs > 60 * 10 / time_scale_factor
                messages = pubsub_client.take_messages() if pubsub_client is not None else []
                jobs_have_changed = False
                for msg in messages:
                    if msg['type'] == 'newPendingJob':
                        jobs_have_changed = True
                    if msg['type'] == 'jobStatusChanged':
                        jobs_have_changed = True
                    if msg['type'] == 'computeResourceAppsChanaged':
                        self._app_manager.update_apps()

                if time_to_handle_jobs or jobs_have_changed:
                    # if time_to_handle_jobs:
                    #     print('Checking for new jobs') # this pollutes the logs too much
                    timer_handle_jobs = time.time()
                    self._handle_jobs()

                self._job_manager.do_work()

                if not reported_that_compute_resource_is_running:
                    print('Compute resource is running')
                    reported_that_compute_resource_is_running = True

                overall_elapsed = time.time() - overall_timer
                if timeout is not None and overall_elapsed > timeout:
                    print(f'Compute resource timed out after {timeout} seconds')
                    return
                if overall_elapsed < 5 / time_scale_factor:
                    time.sleep(0.01 / time_scale_factor) # for the first few seconds we can sleep for a short time (useful for testing)
                else:
                    time.sleep(2 / time_scale_factor)
        finally:
            if cleanup_old_jobs_process is not None:
                cleanup_old_jobs_process.terminate()
            if pubsub_client is not None:
                pubsub_client.close() # unfortunately this doesn't actually stop the thread - it's a pubnub/python issue
    def _handle_jobs(self):
        url_path = f'/api/compute_resource/compute_resources/{self._compute_resource_id}/unfinished_jobs'
        if not self._compute_resource_id:
            return
        if not self._compute_resource_private_key:
            return
        num_tries = 3
        resp = None
        for try_num in range(1, num_tries + 1):
            if try_num > 1:
                print(f'Trying compute resource get api request for {url_path} again. Try number {try_num}')
            try:
                resp = _compute_resource_get_api_request(
                    url_path=url_path,
                    compute_resource_id=self._compute_resource_id,
                    compute_resource_private_key=self._compute_resource_private_key
                )
                break
            except Exception as e:
                print(f'Error in compute resource get api request for {url_path}; {e}')
                if try_num < num_tries:
                    print('Waiting 10 seconds before trying again')
                    time.sleep(10)
                resp = None
        if resp is None:
            return
        jobs = resp['jobs']
        jobs = [DendroJob(**job) for job in jobs]
        self._job_manager.handle_jobs(jobs)

def start_compute_resource(dir: str, *, timeout: Optional[float] = None, cleanup_old_jobs=True): # timeout is used for testing
    # Let's make sure pubnub is installed, because it's required for the daemon
    try:
        import pubnub # noqa
    except ImportError:
        raise ImportError('The pubnub package is not installed. You should use "pip install dendro[compute_resource]".')

    config_fname = os.path.join(dir, '.dendro-compute-resource-node.yaml')
    if os.path.exists(config_fname):
        with open(config_fname, 'r', encoding='utf8') as f:
            the_config = yaml.safe_load(f)
    else:
        the_config = {}
    for k in env_var_keys:
        if k in the_config and the_config[k]:
            os.environ[k] = the_config[k]
        else:
            the_config[k] = ''
    for k in the_config.keys():
        if k not in env_var_keys:
            print('WARNING: Unknown key in config file: ' + k)
    with open(config_fname, 'w', encoding='utf8') as f:
        yaml.dump(the_config, f)
    daemon = Daemon()
    daemon.start(timeout=timeout, cleanup_old_jobs=cleanup_old_jobs)

def get_pubsub_subscription(*, compute_resource_id: str, compute_resource_private_key: str):
    url_path = f'/api/compute_resource/compute_resources/{compute_resource_id}/pubsub_subscription'
    resp = _compute_resource_get_api_request(
        url_path=url_path,
        compute_resource_id=compute_resource_id,
        compute_resource_private_key=compute_resource_private_key
    )
    return resp['subscription']

def _cleanup_old_job_working_directories(dir: str):
    """Delete working dirs that are more than 24 hours old"""
    jobs_dir = Path(dir)
    while True:
        if not jobs_dir.exists():
            continue
        for job_dir in jobs_dir.iterdir():
            if job_dir.is_dir():
                elapsed = time.time() - job_dir.stat().st_mtime
                if elapsed > 24 * 60 * 60:
                    print(f'Removing old working dir {job_dir}')
                    shutil.rmtree(job_dir)
        time.sleep(60)
