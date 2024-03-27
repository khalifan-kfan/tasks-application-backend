import tests.conftest
from app.routes import router
from app.model import Task
import os
import datetime

# from app.tasks import create_celery


task_data = {"title": "testTitle", "creation_date": datetime.datetime.now().isoformat(),
             "author": "testAuthor", "description": "testDescription", "deadline": datetime.datetime.now().isoformat()}


def test_index(test_client):
    response = test_client.get("/api/")
    assert response.status_code == 200

    assert response.json() == {"message": "Welcome to the Cool task api"}


def test_add_task_missing_fields(test_client):
    # Test adding task with missing required fields
    invalid_task_data = {key: value for key,
                         value in task_data.items() if key != "title"}
    response = test_client.post("/api/tasks", json=invalid_task_data)
    assert response.status_code == 422


def test_get_activities(test_client):
    response = test_client.get("/api/tasks")
    assert response.status_code == 200


def test_add_task(test_client):
    response = test_client.post("/api/tasks", json=task_data)
    assert response.status_code == 200


def test_get_task_by_id(test_client):
    add_response = test_client.post("/api/tasks", json=task_data)
    assert add_response.status_code == 200
    added_task_id = add_response.json()["task_id"]
    retrieve_response = test_client.get(f"/api/tasks/{added_task_id}")
    assert retrieve_response.status_code == 200
