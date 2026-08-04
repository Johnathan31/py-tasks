from typing import Optional
from pydantic import BaseModel, Field
from enum import StrEnum


class Priorities(StrEnum):
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    CRITICAL = "critical"

# Pydantic Models


class TaskFields(BaseModel):
    title: str = Field(..., max_length=50)
    priority: Priorities
    done: bool


class TaskOptionalFields(BaseModel):
    title: Optional[str] = Field(None, max_length=50)
    priority: Optional[Priorities] = None
    done: Optional[bool] = None


class TaskIds(BaseModel):
    ids: list[int] | tuple[int, ...]
