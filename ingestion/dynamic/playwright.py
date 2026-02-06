from ingestion.base import IngestionStrategy
from playwright.sync_api import sync_playwright


class PlaywrightIngestionStrategy(IngestionStrategy):
    def fetch(self, source: dict) -> str:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            page.goto(source["url"], timeout=30000)

            # wait_for = source.get("ingestion", {}).get("wait_for")
            # if wait_for:
            #     page.wait_for_selector(
            #         wait_for["selector"],
            #         timeout=wait_for.get("timeout_ms", 10000)
            #     )

            html = page.content()
            browser.close()
            return html
