import logging
from sqlite3 import Row

from fastapi import APIRouter, HTTPException
from fastapi.params import Depends

from starlette import status
from starlette.responses import Response
from fastapi.responses import RedirectResponse

from api.dependencies.cursor import DBDep
from api.dependencies.links import get_short_link
from api.v1.schemas.links import LinkIn, LinkResponse
from db.queries import CREATE_LINK, SELECT_LINK_BY_SOURCE, SELECT_LINK_BY_CODE
from services.links import create_code


logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/links",
    tags=["Links"],
    responses={status.HTTP_404_NOT_FOUND: {"description": "Not found"}},
)


@router.post(
    "/shorten",
    summary="Shorten a link",
    description=(
        "Shorten a link by providing a long URL. The endpoint will return the shortened URL with a 201 status code. If the long URL is already shortened, the endpoint will return the shortened URL with a 200 status code."
    ),
    response_model=LinkResponse,
    responses={
        status.HTTP_200_OK: {"model": LinkResponse},
        status.HTTP_201_CREATED: {"model": LinkResponse},
    },
    status_code=status.HTTP_201_CREATED,
)
async def shorten(db: DBDep, link_in: LinkIn, response: Response):
    source_url = link_in.source_url
    cursor = await db.execute(SELECT_LINK_BY_SOURCE, [str(source_url)])
    link = await cursor.fetchone()
    if link:
        response.status_code = status.HTTP_200_OK
        return LinkResponse(code=link["code"], source_url=source_url)

    while True:
        code = create_code()
        cursor = await db.execute(SELECT_LINK_BY_CODE, (code,))
        if not await cursor.fetchone():
            break
    try:
        await db.execute(CREATE_LINK, (str(source_url), code))
    except Exception as e:
        logger.error("Error creating link", exc_info=e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error creating link")
    return LinkResponse(code=code, source_url=source_url)


@router.get(
    "/{code}",
    summary="Redirect to the original link",
    response_model=None,
    status_code=status.HTTP_301_MOVED_PERMANENTLY,
)
async def redirect_to_link(link: Row = Depends(get_short_link)) -> RedirectResponse:
    return RedirectResponse(link["source_url"], status_code=status.HTTP_301_MOVED_PERMANENTLY)


@router.get("/{code}", summary="", response_model=None, status_code=status.HTTP_301_MOVED_PERMANENTLY)
async def redirect_to_link(link: Row = Depends(get_short_link)) -> RedirectResponse:
    return RedirectResponse(link["source_url"], status_code=status.HTTP_301_MOVED_PERMANENTLY)
