from ingestion.base import IngestionStrategy
from playwright.sync_api import sync_playwright
from ingestion.extractors.registry import EXTRACTOR_REGISTRY
import json
import time


class NetworkJsonIngestionStrategy(IngestionStrategy):
    """
    Ingestion strategy for sites that load job data
    via runtime network (XHR / fetch) JSON responses.
    """

    def fetch(self, source: dict) -> list[dict]:
        responses = []

        def handle_response(response):
            try:
                if self._matches_response(source, response):
                    responses.append(response)
            except Exception:
                pass

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            page.on("response", handle_response)

            page.goto(
                source["url"],
                wait_until="networkidle",
                timeout=30000
            )

            # Give async requests a moment to complete
            time.sleep(2)

            browser.close()

        if not responses:
            print(f"[{source['name']}] ❌ No matching network responses captured")
            return []

        # Take the first matching response (usually enough)
        response = responses[0]

        try:
            data = response.json()
        except Exception:
            print(f"[{source['name']}] ❌ Failed to parse JSON response")
            return []

        extractor_name = source.get("ingestion", {}).get("extractor")
        if not extractor_name:
            print(f"[{source['name']}] ❌ No extractor defined for network_json ingestion")
            return []

        extractor = EXTRACTOR_REGISTRY.get(extractor_name)
        if not extractor:
            print(f"[{source['name']}] ❌ Unknown extractor: {extractor_name}")
            return []

        return extractor(data)

    def _matches_response(self, source: dict, response) -> bool:
        """
        Decide whether a network response is the job API.
        Matching rules are config-driven.
        """
        url_contains = source.get("ingestion", {}).get("response_url_contains")

        if not url_contains:
            return False

        return (
            response.request.resource_type == "xhr"
            and url_contains in response.url
        )
