from typing import Union, List
import traceback
import aiohttp
from fastapi import APIRouter, HTTPException, Header
from .... import BaseModel
from ...services.processor.update_job_status import update_job_status
from ...services.processor.get_upload_url import get_upload_url, get_additional_upload_url, get_upload_url_for_folder_file
from ....common.dendro_types import ProcessorGetJobResponse, ProcessorGetJobResponseInput, ProcessorGetJobResponseOutput, ProcessorGetJobResponseOutputFolder, ProcessorGetJobResponseParameter, ProcessorGetJobResponseInputFolder, ProcessorGetJobResponseInputFolderFile, DendroFile
from ....common.dendro_types import ProcessorGetJobV2Response, ProcessorGetJobV2ResponseInput, ProcessorGetJobV2ResponseInputFolder, GetJobFileInfoResponse
from ...clients.db import fetch_job, fetch_file, fetch_job_private_key
from ...clients.db import _remove_id_field, _get_mongo_client

router = APIRouter()

# get job
# We are going to keep this one for backward compatibility for the time being.
# See processor_get_job_v2 for the new version. And see the note there.
@router.get("/jobs/{job_id}")
async def processor_get_job(job_id: str, job_private_key: str = Header(...)) -> ProcessorGetJobResponse:
    try:
        job = await fetch_job(job_id, include_dandi_api_key=True, include_secret_params=True, include_private_key=True)
        if job is None:
            raise Exception(f"No job with ID {job_id}")

        if job.jobPrivateKey != job_private_key:
            raise Exception(f"Invalid job private key for job {job_id}")
        # after we are done with it, let's delete the private key from the job object for safety
        job.jobPrivateKey = ''

        inputs: List[ProcessorGetJobResponseInput] = []
        input_folders: List[ProcessorGetJobResponseInputFolder] = []
        for input in job.inputFiles:
            file = await fetch_file(project_id=job.projectId, file_name=input.fileName)
            if file is None:
                raise Exception(f"Project file not found: {input.fileName}")
            if file.content.startswith('dendro:?'):
                # this applies to the case where skipCloudUpload is true for the output in the job creating this input file
                url = file.content
            else:
                if not file.content.startswith('url:'):
                    raise Exception(f"Project file content for {input.fileName} is not a URL")
                url = file.content[len('url:'):]
            if not input.isFolder:
                # regular file
                if file.isFolder:
                    raise Exception(f"Mismatch. input is regular file but project file {input.fileName} is a folder")
                url = await _resolve_dandi_url(url, dandi_api_key=job.dandiApiKey)
                inputs.append(ProcessorGetJobResponseInput(
                    name=input.name,
                    url=url
                ))
            else:
                # folder
                if not file.isFolder:
                    raise Exception(f"Mismatch. input is folder but project file {input.fileName} is not a folder")
                file_manifest_obj = await _download_file_manifest_obj(url)
                # get all files in the folder
                folder_files: List[ProcessorGetJobResponseInputFolderFile] = []
                for f in file_manifest_obj['files']:
                    folder_files.append(ProcessorGetJobResponseInputFolderFile(
                        name=f['name'],
                        url=f'{url}/{f["name"]}',
                        size=f.get('size', None)
                    ))
                input_folders.append(ProcessorGetJobResponseInputFolder(
                    name=input.name,
                    files=folder_files
                ))

        outputs: List[ProcessorGetJobResponseOutput] = []
        output_folders: List[ProcessorGetJobResponseOutputFolder] = []
        for output in job.outputFiles:
            if not output.isFolder:
                # regular file
                outputs.append(ProcessorGetJobResponseOutput(
                    name=output.name
                ))
            else:
                # folder
                output_folders.append(ProcessorGetJobResponseOutputFolder(
                    name=output.name
                ))

        parameters: List[ProcessorGetJobResponseParameter] = []
        for parameter in job.inputParameters:
            parameters.append(ProcessorGetJobResponseParameter(
                name=parameter.name,
                value=parameter.value
            ))

        return ProcessorGetJobResponse(
            jobId=job.jobId,
            status=job.status,
            processorName=job.processorName,
            inputs=inputs,
            inputFolders=input_folders,
            outputs=outputs,
            outputFolders=output_folders,
            parameters=parameters
        )
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

# get job v2
# We are going to keep the old one for backward compatibility for the time being
# because existing processor images are built with the old one
# but eventually we will replace it with this one
@router.get("/jobs_v2/{job_id}")
async def processor_get_job_v2(job_id: str, job_private_key: str = Header(...)) -> ProcessorGetJobV2Response:
    try:
        job = await fetch_job(job_id, include_dandi_api_key=True, include_secret_params=True, include_private_key=True)
        if job is None:
            raise Exception(f"No job with ID {job_id}")

        if job.jobPrivateKey != job_private_key:
            raise Exception(f"Invalid job private key for job {job_id}")
        # after we are done with it, let's delete the private key from the job object for safety
        job.jobPrivateKey = ''

        inputs: List[ProcessorGetJobV2ResponseInput] = []
        input_folders: List[ProcessorGetJobV2ResponseInputFolder] = []
        for input in job.inputFiles:
            file = await fetch_file(project_id=job.projectId, file_name=input.fileName)
            if file is None:
                raise Exception(f"Project file not found: {input.fileName}")
            if not input.isFolder:
                # regular file
                if file.isFolder:
                    raise Exception(f"Mismatch. input is regular file but project file {input.fileName} is a folder")
                inputs.append(ProcessorGetJobV2ResponseInput(
                    name=input.name,
                    dendro_uri=f'dendro:?project={job.projectId}&file_id={file.fileId}&label={file.fileName}'
                ))
            else:
                # folder
                if not file.isFolder:
                    raise Exception(f"Mismatch. input is folder but project file {input.fileName} is not a folder")
                input_folders.append(ProcessorGetJobV2ResponseInputFolder(
                    name=input.name,
                    dendro_uri=f'dendro:?project={job.projectId}&file_id={file.fileId}&label={file.fileName}&folder=true',
                ))

        outputs: List[ProcessorGetJobResponseOutput] = []
        output_folders: List[ProcessorGetJobResponseOutputFolder] = []
        for output in job.outputFiles:
            if not output.isFolder:
                # regular file
                outputs.append(ProcessorGetJobResponseOutput(
                    name=output.name,
                    skipCloudUpload=output.skipCloudUpload
                ))
            else:
                # folder
                output_folders.append(ProcessorGetJobResponseOutputFolder(
                    name=output.name,
                    skipCloudUpload=output.skipCloudUpload
                ))

        parameters: List[ProcessorGetJobResponseParameter] = []
        for parameter in job.inputParameters:
            parameters.append(ProcessorGetJobResponseParameter(
                name=parameter.name,
                value=parameter.value
            ))

        return ProcessorGetJobV2Response(
            jobId=job.jobId,
            status=job.status,
            processorName=job.processorName,
            inputs=inputs,
            inputFolders=input_folders,
            outputs=outputs,
            outputFolders=output_folders,
            parameters=parameters
        )
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

async def _resolve_dandi_url(url: str, *, dandi_api_key: Union[str, None]) -> str:
    if url.startswith('https://api.dandiarchive.org/api/') or url.startswith('https://api-staging.dandiarchive.org/api/'):
        headers = {}
        if dandi_api_key is not None:
            headers['Authorization'] = f'token {dandi_api_key}'
        async with aiohttp.ClientSession() as session:
            async with session.head(url, allow_redirects=True, headers=headers) as resp:
                return str(resp.url)
    else:
        return url

# update job status
class ProcessorUpdateJobStatusRequest(BaseModel):
    status: str
    error: Union[str, None] = None
    force_update: Union[bool, None] = None
    output_file_sizes: Union[dict, None] = None

class ProcessorUpdateJobStatusResponse(BaseModel):
    success: bool

@router.put("/jobs/{job_id}/status")
async def processor_update_job_status(job_id: str, data: ProcessorUpdateJobStatusRequest, job_private_key: str = Header(...)) -> ProcessorUpdateJobStatusResponse:
    try:
        job = await fetch_job(job_id, include_private_key=True)
        if job is None:
            raise Exception(f"No job with ID {job_id}")
        if job.jobPrivateKey != job_private_key:
            raise Exception(f"Invalid job private key for job {job_id}")

        await update_job_status(job=job, status=data.status, error=data.error, force_update=data.force_update, output_file_sizes=data.output_file_sizes)

        return ProcessorUpdateJobStatusResponse(success=True)
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

# get job status
class ProcessorGetJobStatusResponse(BaseModel):
    status: Union[str, None] # return None if job does not exist
    success: bool

@router.get("/jobs/{job_id}/status")
async def processor_get_job_status(job_id: str, job_private_key: str = Header(...)) -> ProcessorGetJobStatusResponse:
    try:
        job = await fetch_job(job_id, include_private_key=True)
        if job is None:
            return ProcessorGetJobStatusResponse(status=None, success=True) # pragma: no cover
        if job.jobPrivateKey != job_private_key:
            raise Exception(f"Invalid job private key for job {job_id}") # pragma: no cover

        return ProcessorGetJobStatusResponse(status=job.status, success=True)
    except Exception as e: # pragma: no cover
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

# get job output upload url
class ProcessorGetJobOutputUploadUrlResponse(BaseModel):
    uploadUrl: str
    success: bool

# note that output_name of "_console_output" and "_resource_utilization_log" are special cases
@router.get("/jobs/{job_id}/outputs/{output_name}/upload_url")
async def processor_get_upload_url(job_id: str, output_name: str, job_private_key: str = Header(...)) -> ProcessorGetJobOutputUploadUrlResponse:
    try:
        true_job_private_key = await fetch_job_private_key(job_id)
        assert true_job_private_key, f"No job with ID {job_id}"
        if true_job_private_key != job_private_key:
            raise ValueError(f"Invalid job private key for job {job_id} ({job_private_key})")

        signed_upload_url = await get_upload_url(job_id=job_id, output_name=output_name)
        return ProcessorGetJobOutputUploadUrlResponse(uploadUrl=signed_upload_url, success=True)
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e)) from e

# get job output file ID
class ProcessorGetJobOutputFileIdResponse(BaseModel):
    fileId: str
    success: bool

@router.get("/jobs/{job_id}/outputs/{output_name}/file_id")
async def processor_get_output_file_id(job_id: str, output_name: str, job_private_key: str = Header(...)) -> ProcessorGetJobOutputFileIdResponse:
    try:
        job = await fetch_job(job_id, include_private_key=True)
        if job is None:
            raise Exception(f"No job with ID {job_id}")
        if job.jobPrivateKey != job_private_key:
            raise Exception(f"Invalid job private key for job {job_id}")
        output_file = next((x for x in job.outputFiles if x.name == output_name), None)
        if output_file is None:
            raise Exception(f"No output with name {output_name}")
        file_id = output_file.fileId
        if file_id is None:
            raise Exception(f"Output file ID is None for output {output_name}")
        return ProcessorGetJobOutputFileIdResponse(fileId=file_id, success=True)
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e)) from e

# get job output folder file upload url
class ProcessorGetJobOutputFolderFileUploadUrlResponse(BaseModel):
    uploadUrl: str
    success: bool

@router.get("/jobs/{job_id}/output_folders/{output_folder_name}/files/{file_name:path}/upload_url")
async def processor_get_upload_url_for_output_folder_file(job_id: str, output_folder_name: str, file_name: str, job_private_key: str = Header(...)) -> ProcessorGetJobOutputFolderFileUploadUrlResponse:
    try:
        true_job_private_key = await fetch_job_private_key(job_id)
        assert true_job_private_key, f"No job with ID {job_id}"
        if true_job_private_key != job_private_key:
            raise ValueError(f"Invalid job private key for job {job_id}")

        signed_upload_url = await get_upload_url_for_folder_file(job_id=job_id, output_folder_name=output_folder_name, output_folder_file_name=file_name)
        return ProcessorGetJobOutputFolderFileUploadUrlResponse(uploadUrl=signed_upload_url, success=True)
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e)) from e

# get job output upload url for additional file
class ProcessorGetJobOutputUploadUrlForAdditionalFileResponse(BaseModel):
    uploadUrl: str
    downloadUrl: str
    success: bool

@router.get("/jobs/{job_id}/additional_uploads/sha1/{sha1}/upload_url")
async def processor_get_additional_upload_url(job_id: str, sha1: str, job_private_key: str = Header(...)) -> ProcessorGetJobOutputUploadUrlForAdditionalFileResponse:
    try:
        true_job_private_key = await fetch_job_private_key(job_id)
        assert true_job_private_key, f"No job with ID {job_id}"
        if true_job_private_key != job_private_key:
            raise ValueError(f"Invalid job private key for job {job_id}")

        signed_upload_url, download_url = await get_additional_upload_url(job_id=job_id, sha1=sha1)
        return ProcessorGetJobOutputUploadUrlForAdditionalFileResponse(uploadUrl=signed_upload_url, downloadUrl=download_url, success=True)
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e)) from e

async def _download_file_manifest_obj(folder_url: str):
    url = f'{folder_url}/file_manifest.json'
    print(f'Downloading file manifest from {url}')
    # first, we get the text content
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status != 200:
                raise Exception(f"Error getting file manifest: {resp.status}")
            text = await resp.text()
    # then we parse it
    import json
    return json.loads(text)

# get project file download url

@router.get("/jobs/{job_id}/files/{file_id}")
async def get_job_file_info(job_id: str, file_id: str, job_private_key: str = Header(None)) -> GetJobFileInfoResponse:
    # we use the file id rather than its name within the project in case we want
    # to support renaming of files in the future
    job = await fetch_job(job_id, include_dandi_api_key=True, include_secret_params=True, include_private_key=True)
    if job is None:
        raise Exception(f"No job with ID {job_id}")
    if job.jobPrivateKey != job_private_key:
        raise Exception("Invalid job private key")
    project_id = job.projectId
    dandi_api_key = job.dandiApiKey
    # IMPORTANT: Ideally we would check that the job has access to the file.
    # Primarily we want to allow the job to access all of its inputs. But we
    # also want to allow it to access other files that are ancestors of the
    # inputs, because it could be that the files are json files with
    # embedded URIs that point to those other files. But this is somewhat
    # annoying to implement efficiently, so for now the job will have access
    # to all files in the project. That's not such a huge deal. It's
    # read-only access. So it will probably stay like this for a while, I am
    # guessing.
    file = await fetch_file_by_id(project_id=project_id, file_id=file_id)
    if not file:
        raise Exception(f"No file with ID {file_id} in project {project_id}")
    if file.content.startswith('dendro:?'):
        # this applies to the case where skipCloudUpload is true for the output in the job creating this input file
        url = file.content
    else:
        if not file.content.startswith('url:'):
            raise Exception(f"Project file content for {file_id} is not a URL")
        url = file.content[len('url:'):]
    if dandi_api_key:
        url = await _resolve_dandi_url(url, dandi_api_key=dandi_api_key)
    return GetJobFileInfoResponse(downloadUrl=url, isFolder=file.isFolder if file.isFolder is not None else False, success=True)

async def fetch_file_by_id(project_id: str, file_id: str):
    client = _get_mongo_client()
    files_collection = client['dendro']['files']
    file = await files_collection.find_one({
        'projectId': project_id,
        'fileId': file_id
    })
    _remove_id_field(file)
    if file is None:
        return None
    file = DendroFile(**file) # validate file
    return file
