from fastapi import FastAPI,HTTPException

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
    return tasks.values()


@app.get("/tasks/{task_id}")
def get_task_with_id(task_id: int) -> dict:
    if task_id not in tasks:
        raise HTTPException(status_code=404,detail="Task not found")
    return tasks[task_id]