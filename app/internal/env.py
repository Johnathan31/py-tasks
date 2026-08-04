from dotenv import load_dotenv
from typing import Any, Optional
from os import getenv
from pathlib import Path

env: Path = Path(__file__).parent.parent.parent / ".env"

load_dotenv(dotenv_path=env, override=True)

if not getenv("PASSWORD"):
    raise Exception(
        "\"PASSWORD\" environment variable not provided or empty.")

# Environment Variables

host: str = getenv("HOST") or "localhost"
port: int | Any = getenv("PORT") or 5432
dbname: str = (getenv("DB_NAME") or getenv("DB")) or "tasks"
user: str = getenv("USER") or "postgres"
password: Optional[str] = getenv("PASSWORD")

debug: bool = True if getenv("DEBUG") == "true" else False
