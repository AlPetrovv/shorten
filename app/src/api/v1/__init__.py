from fastapi import APIRouter

from core.config import settings
from .handlers.links import router as links_router

__all__ = ("router",)

router = APIRouter(prefix=settings.api.v1.prefix)

router.include_router(links_router)
