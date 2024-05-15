import time
from typing import List, Union
from ._get_mongo_client import _get_mongo_client
from ._remove_id_field import _remove_id_field
from ...common.dendro_types import DendroProject, DendroFile, DendroJob, DendroComputeResource, ComputeResourceSpec, DendroScript, DendroUser
from ..core._get_project_role import _project_has_user
from ..core._model_dump import _model_dump
from ..core._hide_secret_params_in_job import _hide_secret_params_in_job


async def fetch_projects_for_user(user_id: Union[str, None]) -> List[DendroProject]:
    client = _get_mongo_client()
    projects_collection = client['dendro']['projects']
    projects = await projects_collection.find({}).to_list(length=None) # type: ignore
    for project in projects:
        _remove_id_field(project)
    projects = [DendroProject(**project) for project in projects] # validate projects
    projects2: List[DendroProject] = []
    for project in projects:
        if _project_has_user(project, user_id):
            projects2.append(project)
    return projects2

async def fetch_all_projects() -> List[DendroProject]:
    client = _get_mongo_client()
    projects_collection = client['dendro']['projects']
    projects = await projects_collection.find({}).to_list(length=None) # type: ignore
    for project in projects:
        _remove_id_field(project)
    projects = [DendroProject(**project) for project in projects] # validate projects
    return projects

async def fetch_projects_with_tag(tag: str) -> List[DendroProject]:
    client = _get_mongo_client()
    projects_collection = client['dendro']['projects']
    projects = await projects_collection.find({
        # When you use a query like { "tags": tag } against an array field in MongoDB, it checks if any element of the array matches the value.
        'tags': tag
    }).to_list(length=None) # type: ignore
    for project in projects:
        _remove_id_field(project)
    projects = [DendroProject(**project) for project in projects] # validate projects
    return projects

async def fetch_project(project_id: str, *, raise_on_not_found=False) -> Union[DendroProject, None]:
    client = _get_mongo_client()
    projects_collection = client['dendro']['projects']
    project = await projects_collection.find_one({'projectId': project_id})
    # here I'd like to validate project
    _remove_id_field(project)
    if project is None:
        if raise_on_not_found:
            raise Exception(f"No project with ID {project_id}")
        else:
            return None
    return DendroProject(**project) # validate project

async def fetch_project_files(project_id: str, *, pending_only=False) -> List[DendroFile]:
    client = _get_mongo_client()
    files_collection = client['dendro']['files']
    query = {
        'projectId': project_id
    }
    if pending_only:
        query['content'] = 'pending'
    files = await files_collection.find(query).to_list(length=None) # type: ignore
    for file in files:
        _remove_id_field(file)
    files = [DendroFile(**file) for file in files] # validate files
    return files

async def fetch_multi_project_files(project_ids: List[str], *, pending_only=False) -> List[DendroFile]:
    client = _get_mongo_client()
    files_collection = client['dendro']['files']
    query: dict = {
        'projectId': {'$in': project_ids}
    }
    if pending_only:
        query['content'] = 'pending'
    files = await files_collection.find(query).to_list(length=None) # type: ignore
    for file in files:
        _remove_id_field(file)
    files = [DendroFile(**file) for file in files] # validate files
    return files

async def fetch_project_jobs(project_id: str, include_private_keys=False) -> List[DendroJob]:
    client = _get_mongo_client()
    jobs_collection = client['dendro']['jobs']
    jobs = await jobs_collection.find({
        'projectId': project_id,
        'deleted': {'$ne': True}
    }).to_list(length=None) # type: ignore
    for job in jobs:
        _remove_id_field(job)
    jobs = [DendroJob(**job) for job in jobs] # validate jobs
    if not include_private_keys:
        for job in jobs:
            job.jobPrivateKey = '' # hide the private key
    for job in jobs:
        job.dandiApiKey = None # hide the DANDI API key
        _hide_secret_params_in_job(job)
    return jobs

async def fetch_project_scripts(project_id: str) -> List[DendroScript]:
    client = _get_mongo_client()
    scripts_collection = client['dendro']['scripts']
    scripts = await scripts_collection.find({
        'projectId': project_id
    }).to_list(length=None) # type: ignore
    scripts = [DendroScript(**script) for script in scripts] # validate scripts
    return scripts

async def update_project(project_id: str, update: dict):
    client = _get_mongo_client()
    projects_collection = client['dendro']['projects']
    await projects_collection.update_one({
        'projectId': project_id
    }, {
        '$set': update
    })

async def delete_project(project_id: str):
    client = _get_mongo_client()
    projects_collection = client['dendro']['projects']
    await projects_collection.delete_one({
        'projectId': project_id
    })

async def delete_all_files_in_project(project_id: str):
    client = _get_mongo_client()
    files_collection = client['dendro']['files']
    await files_collection.delete_many({
        'projectId': project_id
    })

async def delete_all_jobs_in_project(project_id: str):
    client = _get_mongo_client()
    jobs_collection = client['dendro']['jobs']
    jobs = await jobs_collection.find({
        'projectId': project_id,
        'deleted': {'$ne': True}
    }).to_list(length=None) # type: ignore
    for job in jobs:
        jobs_collection.update_one({
            'jobId': job['jobId']
        }, {
            '$set': {
                'deleted': True
            }
        })

async def insert_project(project: DendroProject):
    client = _get_mongo_client()
    projects_collection = client['dendro']['projects']
    await projects_collection.insert_one(_model_dump(project, exclude_none=True))

async def fetch_compute_resource(compute_resource_id: str, raise_on_not_found=False):
    client = _get_mongo_client()
    compute_resources_collection = client['dendro']['computeResources']
    compute_resource = await compute_resources_collection.find_one({'computeResourceId': compute_resource_id})
    if compute_resource is None:
        if raise_on_not_found:
            raise ComputeResourceNotFoundError(f"No compute resource with ID {compute_resource_id}")
        else:
            return None # pragma: no cover (not ever run with raise_on_not_found=False)
    _remove_id_field(compute_resource)
    compute_resource = DendroComputeResource(**compute_resource) # validate compute resource
    return compute_resource

async def fetch_compute_resources_for_user(user_id: str):
    client = _get_mongo_client()
    compute_resources_collection = client['dendro']['computeResources']
    compute_resources = await compute_resources_collection.find({'ownerId': user_id}).to_list(length=None) # type: ignore
    for compute_resource in compute_resources:
        _remove_id_field(compute_resource)
    compute_resources = [DendroComputeResource(**compute_resource) for compute_resource in compute_resources] # validate compute resources
    return compute_resources

async def update_compute_resource(compute_resource_id: str, update: dict):
    client = _get_mongo_client()
    compute_resources_collection = client['dendro']['computeResources']
    await compute_resources_collection.update_one({
        'computeResourceId': compute_resource_id
    }, {
        '$set': update
    })

async def delete_compute_resource(compute_resource_id: str):
    client = _get_mongo_client()
    compute_resources_collection = client['dendro']['computeResources']
    await compute_resources_collection.delete_one({
        'computeResourceId': compute_resource_id
    })

async def register_compute_resource(compute_resource_id: str, name: str, user_id: str):
    client = _get_mongo_client()
    compute_resources_collection = client['dendro']['computeResources']

    compute_resource = await compute_resources_collection.find_one({'computeResourceId': compute_resource_id})
    if compute_resource is not None:
        await compute_resources_collection.update_one({'computeResourceId': compute_resource_id}, {
            '$set': {
                'ownerId': user_id,
                'name': name,
                'timestampModified': time.time()
            }
        })
    else:
        new_compute_resource = DendroComputeResource(
            computeResourceId=compute_resource_id,
            ownerId=user_id,
            name=name,
            timestampCreated=time.time(),
            apps=[]
        )
        await compute_resources_collection.insert_one(_model_dump(new_compute_resource, exclude_none=True))

async def fetch_compute_resource_jobs(compute_resource_id: str, statuses: Union[List[str], None], exclude_those_pending_approval: bool = False, include_private_keys: bool = False) -> List[DendroJob]:
    client = _get_mongo_client()
    jobs_collection = client['dendro']['jobs']
    query = {
        'computeResourceId': compute_resource_id,
        'deleted': {'$ne': True}
    }
    if statuses is not None:
        query['status'] = {'$in': statuses}
    if exclude_those_pending_approval:
        query['pendingApproval'] = {'$ne': True}
    jobs = await jobs_collection.find(query).to_list(length=None) # type: ignore
    for job in jobs:
        _remove_id_field(job)
    jobs = [DendroJob(**job) for job in jobs] # validate jobs
    if not include_private_keys:
        for job in jobs:
            job.jobPrivateKey = '' # hide the private key
    for job in jobs:
        job.dandiApiKey = None # hide the DANDI API key
        _hide_secret_params_in_job(job)
    return jobs

class ComputeResourceNotFoundError(Exception):
    pass

async def set_compute_resource_spec(compute_resource_id: str, spec: ComputeResourceSpec):
    client = _get_mongo_client()
    compute_resources_collection = client['dendro']['computeResources']
    compute_resource = await compute_resources_collection.find_one({'computeResourceId': compute_resource_id})
    assert compute_resource is not None, f"No compute resource with ID {compute_resource_id}"
    await compute_resources_collection.update_one({'computeResourceId': compute_resource_id}, {
        '$set': {
            'spec': _model_dump(spec, exclude_none=True)
        }
    })

class JobNotFoundError(Exception):
    pass

async def fetch_job(job_id: str, *, include_dandi_api_key: bool = False, include_secret_params: bool = False, include_private_key: bool = False, raise_on_not_found=False, include_deleted=False):
    client = _get_mongo_client()
    jobs_collection = client['dendro']['jobs']
    job = await jobs_collection.find_one({'jobId': job_id})
    _remove_id_field(job)
    if job is None:
        if raise_on_not_found:
            raise JobNotFoundError(f"No job with ID {job_id}")
        else:
            return None # pragma: no cover (not ever run with raise_on_not_found=False)
    job = DendroJob(**job) # validate job
    if job.deleted and not include_deleted:
        if raise_on_not_found:
            raise JobNotFoundError(f"Job with ID {job_id} has been deleted")
        else:
            return None
    if not include_dandi_api_key:
        job.dandiApiKey = None
    if not include_secret_params:
        _hide_secret_params_in_job(job)
    if not include_private_key:
        job.jobPrivateKey = ''
    return job

job_private_key_cache: dict[str, str] = {}
# expire it every hour
job_private_key_cache_expiration_time = 60 * 60
job_private_key_cache_last_expiration_time = time.time()
def _expire_job_private_key_cache():
    global job_private_key_cache_last_expiration_time
    global job_private_key_cache
    if time.time() - job_private_key_cache_last_expiration_time > job_private_key_cache_expiration_time:
        job_private_key_cache = {}
        job_private_key_cache_last_expiration_time = time.time()

async def fetch_job_private_key(job_id: str):
    _expire_job_private_key_cache()
    if job_id in job_private_key_cache:
        return job_private_key_cache[job_id]
    job = await fetch_job(job_id, include_private_key=True)
    assert job is not None, f"No job with ID {job_id}"
    job_private_key_cache[job_id] = job.jobPrivateKey
    return job.jobPrivateKey

async def update_job(job_id: str, update: dict):
    client = _get_mongo_client()
    jobs_collection = client['dendro']['jobs']
    await jobs_collection.update_one({
        'jobId': job_id
    }, {
        '$set': update
    })

async def delete_job(job_id: str):
    client = _get_mongo_client()
    jobs_collection = client['dendro']['jobs']

    await jobs_collection.update_one({
        'jobId': job_id
    }, {
        '$set': {
            'deleted': True
        }
    })

async def approve_job(job_id: str):
    client = _get_mongo_client()
    jobs_collection = client['dendro']['jobs']

    await jobs_collection.update_one({
        'jobId': job_id
    }, {
        '$set': {
            'pendingApproval': False
        }
    })

async def insert_job(job: DendroJob):
    client = _get_mongo_client()
    jobs_collection = client['dendro']['jobs']
    await jobs_collection.insert_one(_model_dump(job, exclude_none=True))

async def fetch_file(project_id: str, file_name: str):
    client = _get_mongo_client()
    files_collection = client['dendro']['files']
    file = await files_collection.find_one({
        'projectId': project_id,
        'fileName': file_name
    })
    _remove_id_field(file)
    if file is None:
        return None
    file = DendroFile(**file) # validate file
    return file

async def delete_file(project_id: str, file_name: str):
    client = _get_mongo_client()
    files_collection = client['dendro']['files']
    await files_collection.delete_one({
        'projectId': project_id,
        'fileName': file_name
    })

async def insert_file(file: DendroFile):
    client = _get_mongo_client()
    files_collection = client['dendro']['files']
    await files_collection.insert_one(_model_dump(file, exclude_none=True))

async def update_file_metadata(*, project_id, file_id: str, metadata: dict):
    client = _get_mongo_client()
    files_collection = client['dendro']['files']
    await files_collection.update_one({
        'projectId': project_id,
        'fileId': file_id
    }, {
        '$set': {
            'metadata': metadata
        }
    })

class UserNotFoundError(Exception):
    pass

async def fetch_user_for_dendro_api_key(dendro_api_key: str):
    client = _get_mongo_client()
    users_collection = client['dendro']['users']
    user = await users_collection.find_one({
        'dendroApiKey': dendro_api_key
    })
    _remove_id_field(user)
    if user is None:
        raise UserNotFoundError(f"No user with dendro API key {dendro_api_key}")
    user = DendroUser(**user) # validate user
    return user

async def set_dendro_api_key_for_user(user_id: str, dendro_api_key: str):
    client = _get_mongo_client()
    users_collection = client['dendro']['users']
    await users_collection.update_one({
        'userId': user_id
    }, {
        '$set': {
            'dendroApiKey': dendro_api_key
        }
    }, upsert=True)

async def fetch_jobs_including_deleted(*, compute_resource_id: str, user_id: str, include_private_keys=False):
    client = _get_mongo_client()
    jobs_collection = client['dendro']['jobs']
    jobs = await jobs_collection.find({
        'computeResourceId': compute_resource_id,
        'userId': user_id
    }).to_list(length=None) # type: ignore
    for job in jobs:
        _remove_id_field(job)
    jobs = [DendroJob(**job) for job in jobs] # validate jobs
    if not include_private_keys:
        for job in jobs:
            job.jobPrivateKey = '' # hide the private key
    return jobs

async def fetch_files_with_content_string(content_string: str) -> List[DendroFile]:
    client = _get_mongo_client()
    files_collection = client['dendro']['files']
    files = await files_collection.find({
        'content': content_string
    }).to_list(length=None)
    for file in files:
        _remove_id_field(file)
    files = [DendroFile(**file) for file in files] # validate files
    return files

async def fetch_files_with_metadata(metadata_query: dict) -> List[DendroFile]:
    # if it's an empty query, raise an error
    if not metadata_query:
        raise ValueError("metadata_query cannot be empty")
    client = _get_mongo_client()
    files_collection = client['dendro']['files']
    # find files where file['metadata'] matches metadata_query
    files = await files_collection.find({
        'metadata': metadata_query
    }).to_list(length=100)
    for file in files:
        _remove_id_field(file)
    files = [DendroFile(**file) for file in files] # validate files
    return files

class ScriptNotFoundException(Exception):
    pass

async def fetch_script(script_id: str) -> DendroScript:
    client = _get_mongo_client()
    scripts_collection = client['dendro']['scripts']
    script = await scripts_collection.find_one({
        'scriptId': script_id
    })
    if script is None:
        raise ScriptNotFoundException(f"No script with ID {script_id}")
    _remove_id_field(script)
    script = DendroScript(**script) # validate script
    return script

async def delete_script(script_id: str):
    client = _get_mongo_client()
    scripts_collection = client['dendro']['scripts']
    await scripts_collection.delete_one({
        'scriptId': script_id
    })

async def set_script_content(script_id: str, content: str):
    client = _get_mongo_client()
    scripts_collection = client['dendro']['scripts']
    await scripts_collection.update_one({
        'scriptId': script_id
    }, {
        '$set': {
            'content': content
        }
    })

async def rename_script(script_id: str, new_name: str):
    client = _get_mongo_client()
    scripts_collection = client['dendro']['scripts']
    await scripts_collection.update_one({
        'scriptId': script_id
    }, {
        '$set': {
            'scriptName': new_name
        }
    })

async def insert_script(script: DendroScript):
    client = _get_mongo_client()
    scripts_collection = client['dendro']['scripts']
    await scripts_collection.insert_one(_model_dump(script, exclude_none=True))
