import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the To-Do API!"}

def test_add_and_get_task():
    task = {"id": 1, "title": "Learn DevOps", "completed": False}
    response = client.post("/tasks", json=task)
    assert response.status_code == 200
    assert response.json() == task

    response = client.get("/tasks")
    assert response.status_code == 200
    assert task in response.json()

def test_duplicate_task():
    task = {"id": 2, "title": "Learn Testing", "completed": False}
    client.post("/tasks", json=task)
    response = client.post("/tasks", json=task)
    assert response.status_code == 400
    assert response.json()["detail"] == "Task with this ID already exists"

def test_complete_task():
    task = {"id": 3, "title": "Learn Linting", "completed": False}
    client.post("/tasks", json=task)

    response = client.put("/tasks/3")
    assert response.status_code == 200
    assert response.json()["completed"] is True

def test_complete_task_not_found():
    response = client.put("/tasks/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"
