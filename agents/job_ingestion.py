import yaml
from bs4 import BeautifulSoup
from pathlib import Path

from ingestion.static import StaticIngestionStrategy
from ingestion.dynamic.playwright import PlaywrightIngestionStrategy
from ingestion.dynamic.client_state_json import ClientStateJsonIngestionStrategy
from ingestion.dynamic.network_json import NetworkJsonIngestionStrategy

from utils.job_normalizer import normalize_job
from utils.job_store import load_jobs, save_jobs, upsert_jobs


CONFIG_PATH = Path("config/sources.yaml")

# Ingestion strategies
static_ingestor = StaticIngestionStrategy()
dynamic_dom_ingestor = PlaywrightIngestionStrategy()
client_state_ingestor = ClientStateJsonIngestionStrategy()
network_json_ingestor = NetworkJsonIngestionStrategy()


def load_sources():
    print(f"📄 Loading sources from: {CONFIG_PATH.resolve()}")
    with open(CONFIG_PATH, "r") as f:
        return yaml.safe_load(f)


def ingest_source(source: dict) -> list[dict]:
    source_id = source.get("id", source.get("name", "unknown"))
    ingestion_cfg = source.get("ingestion", {})
    mode = ingestion_cfg.get("mode", "static")
    strategy = ingestion_cfg.get("strategy", "dom")

    print(f"\n[{source_id}] Fetching jobs from {source['name']} ({mode}/{strategy})")

    # ------------------------------------------------------------
    # FETCH HTML OR JSON
    # ------------------------------------------------------------
    if mode == "dynamic" and strategy == "dom":
        html = dynamic_dom_ingestor.fetch(source)

    elif mode == "dynamic" and strategy == "network_json":
        raw_jobs = network_json_ingestor.fetch(source)
        print(f"[{source_id}] Found {len(raw_jobs)} jobs via network JSON")
        return raw_jobs

    elif mode == "dynamic" and strategy == "client_state_json":
        raw_jobs = client_state_ingestor.fetch(source)
        print(f"[{source_id}] Found {len(raw_jobs)} jobs via client-state JSON")
        return raw_jobs

    else:
        html = static_ingestor.fetch(source)

    # ------------------------------------------------------------
    # HTML PARSING (INSPECTION MODE)
    # ------------------------------------------------------------
    if "selectors" not in source:
        print(f"[{source_id}] ⏭ Skipped (no selectors defined)")
        return []

    soup = BeautifulSoup(html, "html.parser")

    job_container = source["selectors"].get("job_container", "div")
    cards = soup.select(job_container)

    print(f"[{source_id}] Found {len(cards)} elements for selector '{job_container}'")

    # ------------------------------------------------------------
    # TEMP: DIAGNOSTIC OUTPUT (FIRST 5 ELEMENTS)
    # ------------------------------------------------------------
    for c in cards[:5]:
        print("----")
        print(c.prettify()[:800])

    # ⚠️ We are not extracting jobs yet
    return []


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
