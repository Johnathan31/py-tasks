# Main FastAPI entry point
from contextlib import asynccontextmanager
from fastapi import FastAPI

try:
    from .routes import (
        create,
        read,
        update,
        delete
    )
    from .exceptions import register_exception_handlers
    from .database.connection import pool
    from .internal.env import debug
    from .internal.log import config_logging

except ImportError:
    raise ImportError("Can't import from current path. Run the server from the project root.")

# Application lifespan
@asynccontextmanager
async def lifespan(_: FastAPI):
    config_logging()

    pool.open()

    try:
        yield
    finally:
        pool.close()

# application variable
app: FastAPI = FastAPI(
    debug=debug,
    lifespan=lifespan
)

# Including APIRouters in the same app
app.include_router(create.router)
app.include_router(read.router)
app.include_router(update.router)
app.include_router(delete.router)

register_exception_handlers(app)  # Registering exception handling
