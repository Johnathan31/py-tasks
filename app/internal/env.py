from dotenv import load_dotenv
from typing import Any, Optional
from os import getenv
from pathlib import Path

env: Path = Path(__file__).parent.parent.parent / ".env"

load_dotenv(dotenv_path=env, override=True)

if getenv("POSTGRES_PASSWORD") is None or getenv("POSTGRES_PASSWORD") == "":
    raise Exception("\"POSTGRES_PASSWORD\" environment variable not provided or empty.")

# Environment Variables

dbname: str = getenv("POSTGRES_DB") or "tasks"
user: str = getenv("POSTGRES_USER") or "postgres"
password: Optional[str] = getenv("POSTGRES_PASSWORD")

debug: bool = True if getenv("DEBUG") == "true" else False
