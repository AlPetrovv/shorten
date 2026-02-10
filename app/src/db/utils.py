from typing import AsyncGenerator

from aiosqlite import Cursor

from db.manager import db_manager


async def get_db() -> AsyncGenerator[Cursor]:
    async with db_manager.cursor() as cursor:  # type: Cursor
        yield cursor
