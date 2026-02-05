import requests
from ingestion.base import IngestionStrategy


class StaticIngestionStrategy(IngestionStrategy):
    def fetch(self, source: dict) -> str:
        response = requests.get(source["url"], timeout=15)
        response.raise_for_status()
        return response.text
