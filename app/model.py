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


class TasksFilters(BaseModel):
    title: Optional[str] = Query(None, description="title")
    description: Optional[str] = Query(None, description="description")
    author: Optional[str] = Query(None, description="author")
    deadline: Optional[str] = Query(None, description="deadline")
