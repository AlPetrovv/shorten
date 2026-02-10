import contextlib
import logging
from typing import AsyncIterator

import aiosqlite
from aiosqlite import Connection
from aiosqlite import connect

from core.config import settings

logger = logging.getLogger(__name__)


class DatabaseManager:

    def __init__(self, db_url: str):
        self._db_url = db_url

    async def create_tables(self):
        async with connect(self._db_url) as conn:
            await conn.execute(
                """
                CREATE TABLE IF NOT EXISTS link
                (
                    id         INTEGER PRIMARY KEY AUTOINCREMENT,
                    source_url TEXT NOT NULL,
                    code       TEXT NOT NULL UNIQUE CHECK (length(code) <= 8)
                );
                """
            )

            await conn.execute(
                """
                               CREATE INDEX IF NOT EXISTS idx_link_code
                                   ON link(code);
                               """
            )

            await conn.commit()

    @contextlib.asynccontextmanager
    async def db(self) -> AsyncIterator[Connection]:
        conn = await connect(self._db_url)
        try:
            conn.row_factory = aiosqlite.Row
            yield conn
            await conn.commit()
        except Exception as e:
            await conn.rollback()
            raise
        finally:
            await conn.close()


db_manager = DatabaseManager(db_url=settings.db.url)
