from fastapi import APIRouter, Body

import app.controllers as controllers
from app.model import Task, TaskUpdate
from fastapi import Query
from typing import Optional, Union


router = APIRouter()


@router.get("/")
async def index():
    return {"message": "Welcome to the Cool task api"}


@router.post("/tasks")
def add_task(data: Task = Body(...)):
    return controllers.add_task(data.dict())


@router.get("/tasks")
def get_tasks(
        title: Optional[str] = Query(
            None, description="Title"),
        description: Optional[str] = Query(None, description="Description"),
        author: Optional[str] = Query(None, description="Author"),
        before: Optional[str] = Query(
            None, description="before deadline"),
        after: Optional[str] = Query(None, description="after deadline")):

    return controllers.get_tasks(
        title=title,
        description=description,
        author=author,
        before=before,
        after=after)


@router.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: str) -> Task:
    return controllers.get_single_task(task_id)


@router.patch("/tasks/{task_id}", response_model=dict)
def get_task(task_id: str, data: TaskUpdate = Body(...)):
    # print(data)
    return controllers.update_task(task_id=task_id, task_update=data)
