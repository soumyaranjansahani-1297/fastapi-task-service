from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional
from enum import Enum

class TaskStatus(str, Enum):
    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"

class TaskCreate(BaseModel):
    title: str
    description: str
    status: TaskStatus = TaskStatus.pending

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None

class TaskRead(BaseModel):
    id: int
    title: str
    description: str
    status: TaskStatus
    created_at: datetime

    class Config:
        from_attributes = True

class TaskListResponse(BaseModel):
    total: int
    tasks: List[TaskRead]

class DeleteResponse(BaseModel):
    message: str
