# ingestion/base.py
class IngestionStrategy:
    def fetch(self, source: dict) -> str:
        raise NotImplementedError
