from pydantic import BaseModel
from pydantic import AnyUrl


class LinkIn(BaseModel):
    source_url: AnyUrl


class LinkResponse(BaseModel):
    source_url: AnyUrl
    code: str
