from typing import Annotated
from psycopg import Connection
from fastapi import Depends
from ..internal.models import Priorities
from ..database.dependencies import get_connection


type Conn = Annotated[Connection, Depends(get_connection)]
