import contextlib
import logging
from typing import AsyncIterator

from aiosqlite import Cursor
from aiosqlite import connect

from core.config import settings

logger = logging.getLogger(__name__)


class DatabaseManager:

    def __init__(self, db_url: str):
        self._db_url = db_url

    @contextlib.asynccontextmanager
    async def cursor(self) -> AsyncIterator[Cursor]:
        conn = await connect(self._db_url)
        cursor = None
        try:
            cursor = await conn.cursor()
            yield cursor
            await conn.commit()
        except Exception as e:
            logger.error("DB Error", exc_info=e)
            await conn.rollback()
            raise
        finally:
            if cursor is not None:
                await cursor.close()
            await conn.close()


db_manager = DatabaseManager(db_url=settings.db.url)
