from ingestion.base import IngestionStrategy
from playwright.sync_api import sync_playwright


class StripeIngestionStrategy(IngestionStrategy):
    def fetch(self, source: dict) -> list[dict]:
        """
        Returns a list of RAW job dicts (not HTML).
        Each dict must match the raw ingestion contract.
        """

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            page.goto(source["url"], wait_until="networkidle", timeout=30000)

            # 🔑 Extract Stripe page state
            data = page.evaluate(
                """() => {
                    if (window.__NEXT_DATA__) {
                        return window.__NEXT_DATA__;
                    }
                    return null;
                }"""
            )

            browser.close()

        if not data:
            print("[stripe] ❌ No __NEXT_DATA__ found")
            return []

        return self._extract_jobs_from_next_data(data)

    def _extract_jobs_from_next_data(self, data: dict) -> list[dict]:
        """
        Extract job postings from Stripe's Next.js state.
        This function is intentionally Stripe-specific.
        """

        jobs = []

        # Stripe structure may evolve — we navigate defensively
        try:
            job_nodes = (
                data["props"]["pageProps"]
                .get("jobs", [])
            )
        except Exception:
            print("[stripe] ❌ Unexpected __NEXT_DATA__ structure")
            return []

        for job in job_nodes:
            jobs.append({
                "position": job.get("title"),
                "company": "Stripe",
                "place": job.get("location"),
                "posting_url": f"https://stripe.com/jobs/listing/{job.get('slug')}",
                "source": "stripe"
            })

        return jobs
