import yaml
import requests
from bs4 import BeautifulSoup
from pathlib import Path


CONFIG_PATH = Path("config/sources.yaml")


def load_sources():
    with open(CONFIG_PATH, "r") as f:
        data = yaml.safe_load(f)
    return data.get("sources", [])


def fetch_html(url: str) -> str:
    response = requests.get(url, timeout=15)
    response.raise_for_status()
    return response.text


def ingest_source(source: dict) -> list[dict]:
    print(f"\n[{source['id']}] Fetching jobs from {source['name']}")

    html = fetch_html(source["url"])
    soup = BeautifulSoup(html, "html.parser")

    cards = soup.select(source["selectors"]["job_card"])
    print(f"[{source['id']}] Found {len(cards)} job cards")

    jobs = []

    for card in cards:
        title_el = card.select_one(source["selectors"]["title"])
        link_el = card.select_one(source["selectors"]["link"])
        location_el = card.select_one(source["selectors"]["location"])

        if not title_el or not link_el:
            continue

        job = {
            "position": title_el.get_text(strip=True),
            "company": source["name"].replace(" Careers", ""),
            "place": location_el.get_text(strip=True) if location_el else None,
            "country": source.get("country"),
            "posting_url": link_el.get("href"),
            "source": source["name"],
        }

        jobs.append(job)

    return jobs


def run_ingestion():
    sources = load_sources()
    all_jobs = []

    for source in sources:
        try:
            jobs = ingest_source(source)
            all_jobs.extend(jobs)
        except Exception as e:
            print(f"[{source['id']}] ❌ Failed: {e}")

    return all_jobs
