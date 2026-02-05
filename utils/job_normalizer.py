from datetime import datetime
from urllib.parse import urljoin


def normalize_job(raw_job: dict) -> dict:
    url = raw_job["posting_url"]

    return {
        "id": f"{raw_job['source']}|{url}",
        "source": raw_job["source"],
        "company": raw_job["company"],
        "title": raw_job["position"],
        "location": raw_job.get("place"),
        "url": url,
        "ingested_at": datetime.utcnow().isoformat()
    }
