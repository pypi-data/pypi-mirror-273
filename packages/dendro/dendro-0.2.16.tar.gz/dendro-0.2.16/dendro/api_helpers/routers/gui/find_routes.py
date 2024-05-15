from typing import List
from fastapi import APIRouter
from ..common import api_route_wrapper
from .... import BaseModel
from ....common.dendro_types import DendroProject, DendroFile
from ...clients.db import fetch_files_with_content_string, fetch_project, fetch_files_with_metadata


router = APIRouter()

# find projects
class FindProjectsRequest(BaseModel):
    fileUrl: str

class CreateProjectResponse(BaseModel):
    projects: List[DendroProject]
    success: bool

@router.post("/find_projects")
@api_route_wrapper
async def find_projects(data: FindProjectsRequest) -> CreateProjectResponse:
    files = await fetch_files_with_content_string(f'url:{data.fileUrl}')
    project_ids: List[str] = []
    for file in files:
        if file.projectId not in project_ids:
            project_ids.append(file.projectId)
    projects: List[DendroProject] = []
    for project_id in project_ids:
        p = await fetch_project(project_id)
        if p is not None:
            projects.append(p)
    return CreateProjectResponse(projects=projects, success=True)

# find files with metadata
class FindFilesWithMetadataRequest(BaseModel):
    query: dict

class FindFilesWithMetadataResponse(BaseModel):
    files: List[DendroFile]

@router.post("/find_files_with_metadata")
@api_route_wrapper
async def find_files_with_metadata(data: FindFilesWithMetadataRequest) -> FindFilesWithMetadataResponse:
    files = await fetch_files_with_metadata(data.query)
    return FindFilesWithMetadataResponse(files=files)
