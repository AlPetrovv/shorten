import contextlib

from fastapi import FastAPI


__all__ = ("lifespan",)

from db.manager import db_manager


@contextlib.asynccontextmanager
async def lifespan(app: "FastAPI"):
    await db_manager.create_tables()
    yield
