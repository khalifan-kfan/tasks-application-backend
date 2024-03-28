from typing import Optional
from pydantic import BaseModel
import datetime
from fastapi import Query
from pydantic import BaseModel


class Task(BaseModel):
    title: str
    creation_date: datetime.datetime
    description: str
    author: str
    deadline: datetime.datetime


class TasksGetResponse(BaseModel):
    id: str


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    author: Optional[str] = None
    deadline: Optional[datetime.datetime] = None
