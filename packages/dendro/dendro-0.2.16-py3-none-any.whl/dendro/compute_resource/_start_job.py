import os
import sys
import subprocess
from typing import Union, Dict, Any, Literal

from ..sdk.App import App
from ..common._api_request import _processor_put_api_request
from ..common.dendro_types import DendroJobRequiredResources
from ._run_job_in_aws_batch import _run_job_in_aws_batch
from ..mock import using_mock


class JobException(Exception):
    pass

def _set_job_status_to_starting(*,
    job_id: str,
    job_private_key: str
):
    url_path = f'/api/processor/jobs/{job_id}/status'
    headers = {
        'job-private-key': job_private_key
    }
    data: Dict[str, Any] = {
        'status': 'starting'
    }
    if os.environ.get('DENDRO_FORCE_STATUS_UPDATES', None) == '1':
        data['force_update'] = True # pragma: no cover
    resp = _processor_put_api_request(
        url_path=url_path,
        headers=headers,
        data=data
    )
    if not resp['success']:
        raise JobException(f'Error setting job status to starting: {resp["error"]}') # pragma: no cover

def _start_job(*,
    job_id: str,
    job_private_key: str,
    project_id: str,
    processor_name: str,
    run_method: Literal['local', 'slurm', 'aws_batch'],
    app: App,
    run_process: bool = True,
    return_shell_command: bool = False,
    required_resources: DendroJobRequiredResources
):
    assert not (return_shell_command and run_process), 'Cannot set both run_process and return_shell_command to True'
    assert return_shell_command or run_process, 'Cannot set both run_process and return_shell_command to False'

    _set_job_status_to_starting(
        job_id=job_id,
        job_private_key=job_private_key
    )
    assert hasattr(app, '_app_executable'), 'App does not have an executable path'
    app_executable: Union[str, None] = app._app_executable
    app_image: Union[str, None] = app._app_image

    # default for app_executable
    if app_executable is None:
        assert app_image, 'You must set app_executable if app_image is not set'
        app_executable = '/app/main.py' # the default

    if run_method == 'slurm':
        assert not run_process, 'Not expecting to see run_process here'

    if run_method == 'aws_batch':
        assert not return_shell_command, 'Cannot return shell command for AWS Batch job'
        assert app_image, 'aws_batch_job_queue is set but app_image is not set'
        print(f'Running job in AWS Batch: {job_id} {processor_name}')
        try:
            _run_job_in_aws_batch(
                job_id=job_id,
                job_private_key=job_private_key,
                app_name=app._name,
                container=app_image, # for verifying consistent with job definition
                command=app_executable,
                required_resources=required_resources
            )
        except Exception as e:
            raise JobException(f'Error running job in AWS Batch: {e}') from e
        return ''

    # WARNING!!! The job_dir is going to get cleaned up after the job is finished
    # so it's very important to not set the working directory to a directory that is
    # used for other purposes
    job_dir = os.getcwd() + '/jobs/' + job_id
    os.makedirs(job_dir, exist_ok=True)

    env_vars = {
        'PYTHONUNBUFFERED': '1',
        'JOB_ID': job_id,
        'JOB_PRIVATE_KEY': job_private_key,
        'APP_EXECUTABLE': app_executable,
        'DENDRO_URL': 'https://dendro.vercel.app'
    }

    if required_resources.timeSec is not None:
        env_vars['JOB_TIMEOUT_SEC'] = str(int(required_resources.timeSec))

    # Not doing this any more -- instead we are setting a custom backend for kachery uploads
    # kachery_cloud_client_id, kachery_cloud_private_key = _get_kachery_cloud_credentials()
    # if kachery_cloud_client_id is not None:
    #     env_vars['KACHERY_CLOUD_CLIENT_ID'] = kachery_cloud_client_id
    #     assert kachery_cloud_private_key, 'Unexpected: kachery_cloud_private_key is not set even though kachery_cloud_client_id is set'
    #     env_vars['KACHERY_CLOUD_PRIVATE_KEY'] = kachery_cloud_private_key

    if not app_image:
        # for safety, verify that cleanup directory is as expected
        dendro_job_cleanup_dir = job_dir + '/tmp'
        assert dendro_job_cleanup_dir.endswith('/jobs/' + job_id + '/tmp'), f'Unexpected dendro_job_cleanup_dir: {dendro_job_cleanup_dir}'
        env_vars['DENDRO_JOB_CLEANUP_DIR'] = dendro_job_cleanup_dir # see the warning above
        project_file_cache_dir = os.path.join(os.getcwd(), 'file_cache', 'projects', project_id, 'files')
        os.makedirs(project_file_cache_dir, exist_ok=True)
        env_vars['DENDRO_FILE_CACHE_DIR'] = project_file_cache_dir
        return _run_local_job(
            app_executable=app_executable,
            env_vars=env_vars,
            job_dir=job_dir,
            run_process=run_process,
            return_shell_command=return_shell_command
        )

    return _run_container_job(
        app_executable=app_executable,
        app_image=app_image,
        env_vars=env_vars,
        project_id=project_id,
        job_dir=job_dir,
        run_process=run_process,
        return_shell_command=return_shell_command,
        num_cpus=required_resources.numCpus,
        use_gpu=required_resources.numGpus > 0
        # don't actually limit the memory, because we don't want the process being harshly terminated - it needs to be able to clean up
    )

# This was the method used previously when we wanted to capture the output of the process and display it to the console
# However, that was problematic, because when this parent closes, we don't want a broken pipe
# prefix = f'{job_id} {processor_name}: '
# t1 = threading.Thread(target=stream_output, args=(process.stdout, prefix))
# t1.start()
# prefix = f'{job_id} {processor_name} ERR: '
# t2 = threading.Thread(target=stream_output, args=(process.stderr, prefix))
# t2.start()

# previously did this (see above)
# def stream_output(pipe, prefix: str):
#     while True:
#         try:
#             line = pipe.readline()
#         except:
#             break
#         if line:
#             print(prefix + line.decode('utf-8'))
#         else:
#             break

def _run_local_job(*,
    app_executable: str,
    env_vars: dict,
    job_dir: str,
    run_process: bool,
    return_shell_command: bool,
):
    os.makedirs(job_dir + '/tmp/working', exist_ok=True)
    if using_mock():
        print('Running job directly for mock testing')

        from ..sdk.App import App

        app_instance: App = _load_app_from_main(app_executable)
        try:
            old_environ = {}
            for k, v in env_vars.items():
                old_environ[k] = os.environ.get(k, None)
                os.environ[k] = v

            # Call the make_spec_file method
            print('MOCK: running app instance')
            app_instance.run()
            print('MOCK: Done running app instance')

            for k, v in old_environ.items():
                if v is None:
                    del os.environ[k]
                else:
                    os.environ[k] = v
        finally:
            if 'main' in sys.modules:
                del sys.modules['main'] # important to do this so that at a later time we can load a different main.py

    if run_process:
        if using_mock():
            return
        print(f'Running: {app_executable}')
        subprocess.Popen(
            [app_executable],
            cwd=job_dir + '/tmp/working',
            start_new_session=True, # This is important so it keeps running even if the compute resource is stopped
            # Important to set output to devnull so that we don't get a broken pipe error if this parent process is closed
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            env={
                **os.environ,
                **env_vars
            }
        )
        return ''
    elif return_shell_command:
        env_vars_str = ' '.join([f'{k}={v}' for k, v in env_vars.items()])
        return f'cd {job_dir}/tmp/working && {env_vars_str} APP_EXECUTABLE={app_executable} {app_executable}'
    else:
        return ''

def _run_container_job(*,
    app_executable: str,
    app_image: str,
    env_vars: dict,
    project_id: str,
    job_dir: str,
    run_process: bool,
    return_shell_command: bool,
    num_cpus: Union[int, None],
    use_gpu: bool
):
    project_file_cache_dir = os.path.join(os.getcwd(), 'file_cache', 'projects', project_id, 'files')
    os.makedirs(project_file_cache_dir, exist_ok=True)

    container_method = os.environ.get('CONTAINER_METHOD', 'docker')
    if container_method == 'docker':
        tmpdir = job_dir + '/tmp'
        os.makedirs(tmpdir, exist_ok=True)
        os.makedirs(tmpdir + '/working', exist_ok=True)
        cmd2 = [
            'docker', 'run', '-it'
        ]
        cmd2.extend(['-v', f'{tmpdir}:/tmp'])
        cmd2.extend(['-v', f'{project_file_cache_dir}:/file_cache'])
        env_vars['DENDRO_JOB_CLEANUP_DIR'] = '/tmp'
        env_vars['DENDRO_FILE_CACHE_DIR'] = '/file_cache'
        cmd2.extend(['--workdir', '/tmp/working']) # the working directory will be /tmp/working
        for k, v in env_vars.items():
            cmd2.extend(['-e', f'{k}={v}'])
        # we want kachery temporary files to be stored in the /tmp/.kachery-cloud directory
        cmd2.extend(['-e', 'KACHERY_CLOUD_DIR=/tmp/.kachery-cloud'])
        if num_cpus is not None:
            cmd2.extend(['--cpus', str(num_cpus)])
        if use_gpu:
            cmd2.extend(['--gpus', 'all'])
        cmd2.extend([app_image])
        cmd2.extend([app_executable])
        if run_process:
            print(f'Pulling image {app_image}')
            subprocess.run(['docker', 'pull', app_image])
            print(f'Running: {" ".join(cmd2)}')
            subprocess.Popen(
                cmd2,
                cwd=job_dir,
                start_new_session=True, # This is important so it keeps running even if the compute resource is stopped
                # Important to set output to devnull so that we don't get a broken pipe error if this parent process is closed
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            return ''
        elif return_shell_command:
            return f'cd {job_dir} && {" ".join(cmd2)}'
        else:
            return ''
    elif container_method == 'singularity' or container_method == 'apptainer':
        tmpdir = job_dir + '/tmp' # important to provide a /tmp directory for singularity or apptainer so that it doesn't run out of disk space
        os.makedirs(tmpdir, exist_ok=True)
        os.makedirs(tmpdir + '/working', exist_ok=True)

        # determine the appropriate executable
        if container_method == 'singularity':
            executable = 'singularity'
        elif container_method == 'apptainer':
            executable = 'apptainer'
        else:
            raise JobException(f'Unexpected container method (*): {container_method}')

        cmd2 = [executable, 'exec']
        cmd2.extend(['--bind', f'{tmpdir}:/tmp'])
        cmd2.extend(['--bind', f'{project_file_cache_dir}:/file_cache'])
        # The working directory should be /tmp/working so that if the container wants to write to the working directory, it will not run out of space
        env_vars['DENDRO_JOB_CLEANUP_DIR'] = '/tmp'
        env_vars['DENDRO_FILE_CACHE_DIR'] = '/file_cache'
        cmd2.extend(['--pwd', '/tmp/working'])
        cmd2.extend(['--cleanenv']) # this is important to prevent singularity or apptainer from passing environment variables to the container
        cmd2.extend(['--contain']) # we don't want singularity or apptainer to mount the home or tmp directories of the host
        if use_gpu:
            cmd2.extend(['--nv'])
        for k, v in env_vars.items():
            cmd2.extend(['--env', f'{k}={v}'])
        # we want kachery temporary files to be stored in the /tmp/.kachery-cloud directory
        cmd2.extend(['--env', 'KACHERY_CLOUD_DIR=/tmp/.kachery-cloud'])

        # don't use --cpus for now because we run into cgroups issues and the container fails to start
        # if num_cpus is not None:
        #     cmd2.extend(['--cpus', str(num_cpus)])

        cmd2.extend([f'docker://{app_image}']) # todo: what if it's not a dockerhub image?
        cmd2.extend([app_executable])
        if run_process:
            print(f'Running: {" ".join(cmd2)}')
            subprocess.Popen(
                cmd2,
                cwd=job_dir,
                start_new_session=True, # This is important so it keeps running even if the compute resource is stopped
                # Important to set output to devnull so that we don't get a broken pipe error if this parent process is closed
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            return ''
        elif return_shell_command:
            return f'cd {job_dir} && {" ".join(cmd2)}'
        else:
            return ''
    else:
        raise JobException(f'Unexpected container method: {container_method}')

def _get_kachery_cloud_credentials():
    try:
        from kachery_cloud._client_keys import _get_client_keys_hex
    except ImportError:
        print('Warning: unable to import client keys from kachery_cloud')
        return None, None
    client_id, private_key = _get_client_keys_hex()
    return client_id, private_key

def _load_app_from_main(py_file_path: str) -> App:
    import sys

    # Split the file path into directory and module name (without .py)
    dir_path, file_name = os.path.split(py_file_path)
    module_name = os.path.splitext(file_name)[0]
    if module_name != 'main':
        raise Exception(f'Unexpected module name (expected main): {module_name}')

    # Save the original sys.path
    original_sys_path = [p for p in sys.path] # important to create a copy here

    # Prepend the directory path to sys.path
    sys.path.insert(0, dir_path)

    try:
        import main # type: ignore
        app = main.app
    finally:
        # Restore the original sys.path
        sys.path = original_sys_path

    return app
