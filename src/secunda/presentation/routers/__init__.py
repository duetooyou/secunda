from fastapi import APIRouter

from .buildings import router as buildings_router
from .activities import router as activities_router
from .organizations import router as organizations_router

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(buildings_router)
api_router.include_router(activities_router)
api_router.include_router(organizations_router)

__all__ = ["api_router"]
