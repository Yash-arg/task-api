from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


class TaskCreate(BaseModel):
    title: str
    description: str
    priority: str


class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    status: str | None = None
    priority: str | None = None


app = FastAPI()

tasks = {
    1: {
        "id": 1,
        "title": "Learn HTTP",
        "description": "Understand methods, status codes and headers",
        "status": "done",
        "priority": "high",
    },
    2: {
        "id": 2,
        "title": "Build first FastAPI server",
        "description": "Create /health and task routes",
        "status": "in_progress",
        "priority": "high",
    },
    3: {
        "id": 3,
        "title": "Write README",
        "description": "Document how to run the API",
        "status": "todo",
        "priority": "medium",
    },
    4: {
        "id": 4,
        "title": "Clean up expense tracker",
        "description": "Apply mentor feedback",
        "status": "todo",
        "priority": "low",
    },
}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/tasks")
def get_tasks() -> list[dict]:
    return list(tasks.values())


@app.get("/tasks/{task_id}")
def get_task_with_id(task_id: int) -> dict:
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    return tasks[task_id]


@app.post("/add_tasks", status_code=201)
def create_task(task: TaskCreate) -> dict:
    if not tasks:
        new_task_id = 1
    else:
        new_task_id = max(tasks.keys()) + 1
    new_task = task.model_dump()
    new_task["id"] = new_task_id
    new_task["status"] = "todo"
    tasks[new_task_id] = new_task
    return new_task


@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    if task_id not in tasks:
        raise HTTPException(
            status_code=404, detail=f"No tasks with task_id: {task_id} found"
        )
    tasks.pop(task_id)


@app.patch("/tasks/{task_id}")
def update_task(task_id: int, update: TaskUpdate) -> dict:
    if task_id not in tasks:
        raise HTTPException(
            status_code=404, detail=f"No tasks with task_id: {task_id} found"
        )
    changes = update.model_dump(exclude_unset=True)
    tasks[task_id].update(changes)
    return tasks[task_id]
