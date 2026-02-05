import yaml
from bs4 import BeautifulSoup
from pathlib import Path

from ingestion.static import StaticIngestionStrategy
from ingestion.dynamic.playwright import PlaywrightIngestionStrategy

CONFIG_PATH = Path("config/sources.yaml")

static_ingestor = StaticIngestionStrategy()
dynamic_ingestor = PlaywrightIngestionStrategy()


def load_sources():
    print(f"📄 Loading sources from: {CONFIG_PATH.resolve()}")
    with open(CONFIG_PATH, "r") as f:
        data = yaml.safe_load(f)
    return data


def ingest_source(source: dict) -> list[dict]:
    source_id = source.get("id", source.get("name", "unknown"))
    mode = source.get("ingestion", {}).get("mode", "static")

    if "selectors" not in source:
        print(f"[{source_id}] ⏭ Skipped (no selectors defined)")
        return []

    print(f"\n[{source_id}] Fetching jobs from {source['name']} ({mode})")

    # 🔑 SELECT INGESTION STRATEGY
    if mode == "dynamic":
        html = dynamic_ingestor.fetch(source)
    else:
        html = static_ingestor.fetch(source)

    soup = BeautifulSoup(html, "html.parser")

    # 🔒 SAFE ACCESS TO job_container
    job_container = source["selectors"].get("job_container")
    if not job_container:
        print(f"[{source_id}] ⏭ Skipped (no job_container selector)")
        return []

    cards = soup.select(job_container)

    if not cards:
        print(f"[{source_id}] 🔍 No job cards found. Printing page sample:")
        print(soup.prettify()[:2000])

    print(f"[{source_id}] Found {len(cards)} job cards")

    jobs = []

    for card in cards:
        title_selector = source["selectors"].get("title")
        link_selector = source["selectors"].get("link")
        location_selector = source["selectors"].get("location")

        title_el = card.select_one(title_selector) if title_selector else None
        link_el = card.select_one(link_selector) if link_selector else None
        location_el = card.select_one(location_selector) if location_selector else None

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
            source_id = source.get("id", source.get("name", "unknown"))
            print(f"[{source_id}] ❌ Failed: {e}")

    return all_jobs
