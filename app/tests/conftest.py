"""Shared fixtures for the py-tasks API tests.

Set TEST_DATABASE_URL to a dedicated PostgreSQL test database with
app/schema.sql already applied. These tests delete test rows before and
after each test, so never point TEST_DATABASE_URL at production data.
"""
import asyncio
import os
from collections.abc import Callable
from typing import Any

import httpx
import psycopg
import pytest
from psycopg.rows import dict_row

from dotenv import load_dotenv

# The application validates POSTGRES_PASSWORD while importing its settings.
os.environ.setdefault("POSTGRES_PASSWORD", "test-import-only")
os.environ.setdefault("POSTGRES_DB", "tasks")
os.environ.setdefault("POSTGRES_USER", "postgres")

from ..main import app  # noqa: E402
from ..database.dependencies import get_connection  # noqa: E402

load_dotenv()

@pytest.fixture
def database_url() -> str:
    url = os.getenv("TEST_DATABASE_URL")
    if not url:
        pytest.fail(
            "Set TEST_DATABASE_URL to a dedicated PostgreSQL test database. "
            "Do not point it at a production database."
        )
    return url


@pytest.fixture
def clean_test_database(database_url: str):
    """Keep each test independent by clearing rows around the test."""
    with psycopg.connect(database_url, row_factory=dict_row) as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT to_regclass('public.tasks') AS table_name")
            if cursor.fetchone()["table_name"] is None:
                pytest.fail(
                    "The test database has no public.tasks table. "
                    "Initialize this dedicated database with app/schema.sql first."
                )
            cursor.execute("DELETE FROM tasks")
    yield
    with psycopg.connect(database_url, row_factory=dict_row) as connection:
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM tasks")


@pytest.fixture
def client(database_url: str, clean_test_database) -> Callable[..., httpx.Response]:
    """HTTPX ASGI client; each request gets a normal, independent DB transaction."""

    def override_get_connection():
        with psycopg.connect(database_url, row_factory=dict_row) as connection:
            yield connection

    app.dependency_overrides[get_connection] = override_get_connection
    transport = httpx.ASGITransport(app=app)

    def request(method: str, path: str, **kwargs: Any) -> httpx.Response:
        async def send_request() -> httpx.Response:
            async with httpx.AsyncClient(
                transport=transport,
                base_url="http://testserver",
            ) as async_client:
                return await async_client.request(method, path, **kwargs)

        return asyncio.run(send_request())

    try:
        yield request
    finally:
        app.dependency_overrides.pop(get_connection, None)
