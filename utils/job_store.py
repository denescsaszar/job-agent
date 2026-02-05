import json
from pathlib import Path

DATA_PATH = Path("data/jobs_raw.json")


def load_jobs() -> dict:
    if not DATA_PATH.exists():
        return {}
    with open(DATA_PATH, "r") as f:
        return json.load(f)


def save_jobs(jobs: dict):
    DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(DATA_PATH, "w") as f:
        json.dump(jobs, f, indent=2)


def upsert_jobs(existing: dict, new_jobs: list[dict]) -> dict:
    for job in new_jobs:
        existing[job["id"]] = job
    return existing
