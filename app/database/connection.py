from psycopg.rows import dict_row
from psycopg_pool import ConnectionPool
from ..internal.env import host, port, dbname, user, password

# Database connection
pool = ConnectionPool(
    conninfo=(
        f"host={host} "
        f"dbname={dbname} "
        f"port={port} "
        f"user={user} "
        f"password={password}"
    ),
    min_size=2,
    max_size=10,
    open=False,
    kwargs={"row_factory": dict_row}
)
