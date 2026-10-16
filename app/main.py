from fastapi import FastAPI, HTTPException

from app import services
from app.models import Priority, Status, TaskCreate, TaskUpdate

app = FastAPI()


def not_found(task_id: int) -> HTTPException:
    return HTTPException(
        status_code=404, detail=f"No tasks with task_id: {task_id} found"
    )


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/tasks")
def get_tasks(
    status: Status | None = None, priority: Priority | None = None
) -> list[dict]:
    return services.list_tasks(status, priority)


@app.get("/tasks/{task_id}")
def get_task_with_id(task_id: int) -> dict:
    task = services.get_task(task_id)
    if task is None:
        raise not_found(task_id)
    return task


@app.post("/tasks", status_code=201)
def create_task(task: TaskCreate) -> dict:
    return services.create_task(task)


@app.patch("/tasks/{task_id}")
def update_task(task_id: int, update: TaskUpdate) -> dict:
    updated = services.update_task(task_id, update)
    if updated is None:
        raise not_found(task_id)
    return updated


@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    if not services.delete_task(task_id):
        raise not_found(task_id)