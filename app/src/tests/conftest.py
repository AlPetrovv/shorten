from typing import AsyncGenerator

import pytest
import pytest_asyncio
from aiosqlite import Connection
from httpx import AsyncClient, ASGITransport


from db.manager import db_manager
from db.utils import get_db
from main import create_app

from tests.links.fixtures import *  # noqa


@pytest_asyncio.fixture(scope="session", autouse=True)
async def init_db_manager():
    await db_manager.create_tables()
    yield
    await db_manager.drop_tables()


# Required per https://anyio.readthedocs.io/en/stable/testing.html#using-async-fixtures-with-higher-scopes
@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest_asyncio.fixture(scope="session")
async def api_client() -> AsyncGenerator[AsyncClient]:
    app = create_app()

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test/api/v1") as client:
        yield client
