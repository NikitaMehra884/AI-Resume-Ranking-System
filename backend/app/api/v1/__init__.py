from fastapi import APIRouter
from backend.app.api.v1.auth import router as auth_router
from backend.app.api.v1.jobs import router as jobs_router
from backend.app.api.v1.candidates import router as candidates_router
from backend.app.api.v1.screening import router as screening_router
from backend.app.api.v1.analytics import router as analytics_router

api_v1_router = APIRouter()
api_v1_router.include_router(auth_router)
api_v1_router.include_router(jobs_router)
api_v1_router.include_router(candidates_router)
api_v1_router.include_router(screening_router)
api_v1_router.include_router(analytics_router)
