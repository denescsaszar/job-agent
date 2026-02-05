from ingestion.base import IngestionStrategy
from playwright.sync_api import sync_playwright
from ingestion.extractors.registry import EXTRACTOR_REGISTRY


class ClientStateJsonIngestionStrategy(IngestionStrategy):
    """
    Ingestion strategy for sites that expose job data
    via client-side JSON state (e.g. window.__NEXT_DATA__).
    """

    STATE_KEYS = [
        "__NEXT_DATA__",
        "__APOLLO_STATE__",
        "__NUXT__",
    ]

    def fetch(self, source: dict) -> list[dict]:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            page.goto(source["url"], wait_until="networkidle", timeout=30000)

            state = page.evaluate(
                """(keys) => {
                    for (const key of keys) {
                        if (window[key]) {
                            return { key, data: window[key] };
                        }
                    }
                    return null;
                }""",
                self.STATE_KEYS,
            )

            browser.close()

        if not state:
            print(f"[{source['name']}] ❌ No client-side JSON state found")
            return []

        extractor_name = source.get("ingestion", {}).get("extractor")
        if not extractor_name:
            print(f"[{source['name']}] ❌ No extractor defined for client-state ingestion")
            return []

        extractor = EXTRACTOR_REGISTRY.get(extractor_name)
        if not extractor:
            print(f"[{source['name']}] ❌ Unknown extractor: {extractor_name}")
            return []

        return extractor(state["data"])
