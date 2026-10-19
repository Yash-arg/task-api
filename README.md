# Task Management API

A REST API for managing tasks, built with Python and FastAPI. Tasks can be created, listed, filtered, updated and deleted, and are saved to a JSON file so they survive server restarts.

## Features

- Create, read, update and delete tasks
- Filter tasks by status and priority, separately or combined
- Validation of allowed values for status and priority
- Empty titles are rejected
- Partial updates with PATCH, where only the fields sent are changed
- Automatic `created_at` and `updated_at` timestamps
- Clear error responses (404 for missing tasks, 422 for invalid input)
- Persistent storage in `data/tasks.json`
- Interactive API docs at `/docs`

## Task Fields

| Field | Type | Set by | Notes |
|---|---|---|---|
| `id` | integer | server | unique task id |
| `title` | string | client | required, at least 1 character |
| `description` | string or null | client | optional |
| `status` | string | server on create, client on update | `todo`, `in_progress` or `done` |
| `priority` | string | client | `low`, `medium` or `high` |
| `created_at` | string | server | ISO 8601 timestamp |
| `updated_at` | string | server | ISO 8601 timestamp, changes on every update |

New tasks always start with status `todo`.

## Installation

Requires Python 3.10 or newer.

```bash
git clone https://github.com/Yash-arg/task-api.git
cd task-api
python -m venv .venv
```

Activate the virtual environment:

```bash
.venv\Scripts\Activate.ps1
```

On macOS or Linux:

```bash
source .venv/bin/activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

## Running the Server

From the `task-api` folder:

```bash
uvicorn app.main:app --reload
```

The API runs at `http://localhost:8000`, and the interactive docs are at `http://localhost:8000/docs`.

## Endpoints

| Method | Path | Description | Success |
|---|---|---|---|
| GET | `/health` | Health check | 200 |
| GET | `/tasks` | List all tasks | 200 |
| GET | `/tasks?status=todo` | Filter by status | 200 |
| GET | `/tasks?priority=high` | Filter by priority | 200 |
| GET | `/tasks?status=todo&priority=high` | Filter by both | 200 |
| GET | `/tasks/{id}` | Get one task | 200 |
| POST | `/tasks` | Create a task | 201 |
| PATCH | `/tasks/{id}` | Update some fields of a task | 200 |
| DELETE | `/tasks/{id}` | Delete a task | 204 |

### Error Responses

| Status | When |
|---|---|
| 404 Not Found | The task id does not exist |
| 422 Unprocessable Content | Missing or invalid fields, invalid filter values, malformed JSON, or a non-integer id |

In a PATCH request, fields sent as `null` are ignored, so existing values cannot be wiped by accident.

## Example Requests

The examples below use the request bodies stored in the `requests/` folder. On Windows PowerShell, use `curl.exe` instead of `curl`.

Create a task:

```bash
curl -i -X POST http://localhost:8000/tasks -H "Content-Type: application/json" -d "@requests/create_task.json"
```

Response:

```json
{
  "title": "Learn backend engineering",
  "description": "Finish Week 2",
  "priority": "high",
  "id": 5,
  "status": "todo",
  "created_at": "2026-10-19T10:21:45.148463",
  "updated_at": "2026-10-19T10:21:45.148463"
}
```

List all tasks:

```bash
curl -i http://localhost:8000/tasks
```

Filter tasks:

```bash
curl -i "http://localhost:8000/tasks?status=todo&priority=low"
```

Get one task:

```bash
curl -i http://localhost:8000/tasks/5
```

Update a task:

```bash
curl -i -X PATCH http://localhost:8000/tasks/5 -H "Content-Type: application/json" -d "@requests/patch_status.json"
```

Delete a task:

```bash
curl -i -X DELETE http://localhost:8000/tasks/5
```

### Error Examples

| Request | Status |
|---|---|
| `curl -i http://localhost:8000/tasks/999` | 404 |
| `curl -i "http://localhost:8000/tasks?status=banana"` | 422 |
| `curl -i http://localhost:8000/tasks/abc` | 422 |
| POST with `requests/missing_title.json` | 422 |
| POST with `requests/invalid_priority.json` | 422 |
| POST with `requests/empty_title.json` | 422 |
| POST with `requests/malformed.json` | 422 |
| PATCH with `requests/patch_empty.json` | 422 |

## Project Structure

```
task-api/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── models.py
│   ├── services.py
│   └── storage.py
├── data/
│   └── tasks.json
├── requests/
├── tests/
├── README.md
└── requirements.txt
```

| File | Responsibility |
|---|---|
| `app/main.py` | Routes, HTTP status codes and 404 errors |
| `app/models.py` | Pydantic models that validate request bodies |
| `app/services.py` | Task logic: filtering, creating, updating and deleting |
| `app/storage.py` | Loading tasks from and saving tasks to the JSON file |
| `data/tasks.json` | Stored tasks |
| `requests/` | Example request bodies for testing with curl |

## Limitations

Storage is a single JSON file that is rewritten on every change. This is fine for learning, but it does not handle concurrent writes safely and does not scale to large numbers of tasks. It will be replaced with PostgreSQL.