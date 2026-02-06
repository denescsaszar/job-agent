import requests
from ingestion.base import IngestionStrategy


class HttpJsonIngestionStrategy(IngestionStrategy):
    """
    Ingestion strategy for public HTTP JSON APIs
    (no Playwright, no browser).
    """

    def fetch(self, source: dict) -> list[dict]:
        url = source["url"]
        params = source.get("ingestion", {}).get("params", {})

        print(f"[{source['name']}] 🌐 Fetching JSON via HTTP")

        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()

        data = response.json()

        extractor_name = source.get("ingestion", {}).get("extractor")
        if not extractor_name:
            print(f"[{source['name']}] ❌ No extractor defined")
            return []

        from ingestion.extractors.registry import EXTRACTOR_REGISTRY

        extractor = EXTRACTOR_REGISTRY.get(extractor_name)
        if not extractor:
            print(f"[{source['name']}] ❌ Unknown extractor: {extractor_name}")
            return []

        jobs = extractor(data)
        print(f"[{source['name']}] Found {len(jobs)} jobs via HTTP JSON")

        return jobs
