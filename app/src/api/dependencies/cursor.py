from typing import Annotated

from aiosqlite import Connection
from fastapi import Depends

from db.utils import get_db

DBDep = Annotated[Connection, Depends(get_db)]
