from typing import Literal

from pydantic import BaseModel, Field

Status = Literal["todo", "in_progress", "done"]
Priority = Literal["high", "medium", "low"]


class TaskCreate(BaseModel):
    title: str = Field(min_length=1)
    description: str | None = None
    priority: Priority


class TaskUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1)
    description: str | None = None
    status: Status | None = None
    priority: Priority | None = None
