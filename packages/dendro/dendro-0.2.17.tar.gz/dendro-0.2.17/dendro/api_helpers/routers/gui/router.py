from fastapi import APIRouter
from .create_job_route import router as create_job_router
from .project_routes import router as project_router
from .compute_resource_routes import router as compute_resource_router
from .file_routes import router as file_router
from .job_routes import router as job_router
from .script_routes import router as script_router
from .github_auth_routes import router as github_auth_router
from .user_routes import router as user_router
from .usage_routes import router as usage_router
from .find_routes import router as find_router

router = APIRouter()

router.include_router(create_job_router)
router.include_router(project_router, prefix="/projects")
router.include_router(compute_resource_router, prefix="/compute_resources")
router.include_router(file_router)
router.include_router(job_router, prefix="/jobs")
router.include_router(script_router, prefix="/scripts")
router.include_router(github_auth_router)
router.include_router(user_router, prefix="/users")
router.include_router(usage_router, prefix="/usage")
router.include_router(find_router)
