from typing import AsyncGenerator

from aiosqlite import Connection

from db.manager import db_manager


async def get_db() -> AsyncGenerator[Connection]:
    async with db_manager.db() as db:  # type: Connection
        yield db
