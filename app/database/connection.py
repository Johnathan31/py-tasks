from psycopg.rows import dict_row
from psycopg_pool import ConnectionPool
from ..internal.env import dbname, user, password

# Database connection
pool = ConnectionPool(
    conninfo=(
        f"host=db "
        f"dbname={dbname} "
        f"port=5432 "
        f"user={user} "
        f"password={password}"
    ),
    min_size=2,
    max_size=10,
    open=False,
    kwargs={"row_factory": dict_row}
)
