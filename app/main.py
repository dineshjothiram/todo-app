from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# In-memory database
tasks = []

class Task(BaseModel):
    id: int
    title: str
    completed: bool = False

@app.get("/")
def read_root():
    return {"message": "Welcome to the To-Do API!"}

@app.get("/tasks")
def get_tasks():
    return tasks

@app.post("/tasks")
def add_task(task: Task):
    for t in tasks:
        if t["id"] == task.id:
            raise HTTPException(status_code=400, detail="Task with this ID already exists")
    tasks.append(task.dict())
    return task

@app.put("/tasks/{task_id}")
def complete_task(task_id: int):
    for t in tasks:
        if t["id"] == task_id:
            t["completed"] = True
            return t
    raise HTTPException(status_code=404, detail="Task not found")
