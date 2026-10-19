import json

DATA_FILE = "data/tasks.json"


def load_tasks() -> dict[int, dict]:
    try:
        with open(DATA_FILE) as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}
    return {int(k): v for k, v in data.items()}


def save_tasks(tasks: dict[int, dict]) -> None:
    with open(DATA_FILE, "w") as f:
        json.dump(tasks, f, indent=2)
