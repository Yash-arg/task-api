from datetime import datetime

from app.models import Priority, Status, TaskCreate, TaskUpdate

tasks: dict[int, dict] = {
    1: {
        "id": 1,
        "title": "Learn HTTP",
        "description": "Understand methods, status codes and headers",
        "status": "done",
        "priority": "high",
        "created_at": "2026-10-10T09:00:00",
        "updated_at": "2026-10-11T18:30:00",
    },
    2: {
        "id": 2,
        "title": "Build first FastAPI server",
        "description": "Create /health and task routes",
        "status": "in_progress",
        "priority": "high",
        "created_at": "2026-10-11T10:15:00",
        "updated_at": "2026-10-12T21:00:00",
    },
    3: {
        "id": 3,
        "title": "Write README",
        "description": "Document how to run the API",
        "status": "todo",
        "priority": "medium",
        "created_at": "2026-10-12T11:00:00",
        "updated_at": "2026-10-12T11:00:00",
    },
    4: {
        "id": 4,
        "title": "Clean up expense tracker",
        "description": "Apply mentor feedback",
        "status": "todo",
        "priority": "low",
        "created_at": "2026-10-13T08:45:00",
        "updated_at": "2026-10-13T08:45:00",
    },
}


def list_tasks(
    status: Status | None = None, priority: Priority | None = None
) -> list[dict]:
    """Return all tasks, optionally filtered by status and/or priority."""
    result = list(tasks.values())
    if status is not None:
        result = [t for t in result if t["status"] == status]
    if priority is not None:
        result = [t for t in result if t["priority"] == priority]
    return result


def get_task(task_id: int) -> dict | None:
    """Return one task, or None if it doesn't exist."""
    return tasks.get(task_id)


def create_task(task: TaskCreate) -> dict:
    """Build a new task from the client's data plus server-set fields."""
    if not tasks:
        new_task_id = 1
    else:
        new_task_id = max(tasks.keys()) + 1
    new_task = task.model_dump()
    now = datetime.now().isoformat()
    new_task["id"] = new_task_id
    new_task["status"] = "todo"
    new_task["created_at"] = now
    new_task["updated_at"] = now
    tasks[new_task_id] = new_task
    return new_task


def update_task(task_id: int, update: TaskUpdate) -> dict | None:
    """Apply only the fields the client sent. Returns None if the task doesn't exist."""
    if task_id not in tasks:
        return None
    changes = update.model_dump(exclude_unset=True,exclude_none=True)
    tasks[task_id].update(changes)
    tasks[task_id]["updated_at"] = datetime.now().isoformat()
    return tasks[task_id]


def delete_task(task_id: int) -> bool:
    """Delete a task. Returns True if it was deleted, False if it didn't exist."""
    if task_id not in tasks:
        return False
    tasks.pop(task_id)
    return True