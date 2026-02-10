from typing import Annotated


from fastapi import HTTPException, Path
from starlette import status

from api.dependencies.cursor import DBDep
from db.queries import SELECT_LINK_BY_CODE


async def get_short_link(code: Annotated[str, Path(max_length=8, min_length=8)], db: DBDep) -> dict:
    """
    Retrieve a short link by its code.

    :param code: The code of the short link.
    :type code: str
    :param db: The database connection.
    :type db: aiosqlite.Connection
    :return: The short link.
    :rtype: dict
    :raises fastapi.HTTPException: If the short link is not found.
    """
    """"""
    cursor = await db.execute(SELECT_LINK_BY_CODE, [code])
    link = await cursor.fetchone()
    if link is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Link not found")
    return link
