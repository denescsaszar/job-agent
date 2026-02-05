import yaml
from bs4 import BeautifulSoup
from pathlib import Path

from ingestion.static import StaticIngestionStrategy
from ingestion.dynamic.playwright import PlaywrightIngestionStrategy
from ingestion.dynamic.client_state_json import ClientStateJsonIngestionStrategy

from utils.job_normalizer import normalize_job
from utils.job_store import load_jobs, save_jobs, upsert_jobs

CONFIG_PATH = Path("config/sources.yaml")

static_ingestor = StaticIngestionStrategy()
dynamic_ingestor = PlaywrightIngestionStrategy()
client_state_ingestor = ClientStateJsonIngestionStrategy()


def load_sources():
    print(f"📄 Loading sources from: {CONFIG_PATH.resolve()}")
    with open(CONFIG_PATH, "r") as f:
        data = yaml.safe_load(f)
    return data


def ingest_source(source: dict) -> list[dict]:
    source_id = source.get("id", source.get("name", "unknown"))
    ingestion_cfg = source.get("ingestion", {})
    mode = ingestion_cfg.get("mode", "static")
    strategy = ingestion_cfg.get("strategy")

    print(f"\n[{source_id}] Fetching jobs from {source['name']} ({mode})")

    # 🔑 CLIENT-SIDE JSON INGESTION (Stripe-style)
    if mode == "dynamic" and strategy == "client_state_json":
        raw_jobs = client_state_ingestor.fetch(source)
        print(f"[{source_id}] Found {len(raw_jobs)} jobs via client-state JSON")
        return raw_jobs

    # 🔑 HTML-BASED INGESTION (static or dynamic DOM)
    if "selectors" not in source:
        print(f"[{source_id}] ⏭ Skipped (no selectors defined)")
        return []

    if mode == "dynamic":
        html = dynamic_ingestor.fetch(source)
    else:
        html = static_ingestor.fetch(source)

    soup = BeautifulSoup(html, "html.parser")

    job_container = source["selectors"].get("job_container")
    if not job_container:
        print(f"[{source_id}] ⏭ Skipped (no job_container selector)")
        return []

    cards = soup.select(job_container)

    if not cards:
        print(f"[{source_id}] 🔍 No job cards found")
        return []

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

        jobs.append({
            "position": title_el.get_text(strip=True),
            "company": source["name"].replace(" Careers", ""),
            "place": location_el.get_text(strip=True) if location_el else None,
            "country": source.get("country"),
            "posting_url": link_el.get("href"),
            "source": source["name"],
        })

    return jobs


def run_ingestion():
    sources = load_sources()

    existing_jobs = load_jobs()
    normalized_jobs = []

    for source in sources:
        try:
            raw_jobs = ingest_source(source)
            for raw_job in raw_jobs:
                normalized_jobs.append(normalize_job(raw_job))
        except Exception as e:
            source_id = source.get("id", source.get("name", "unknown"))
            print(f"[{source_id}] ❌ Failed: {e}")

    updated_jobs = upsert_jobs(existing_jobs, normalized_jobs)
    save_jobs(updated_jobs)

    print(f"\n💾 Stored {len(updated_jobs)} total jobs locally")

    return normalized_jobs
