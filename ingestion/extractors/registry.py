from ingestion.extractors.stripe import extract_stripe_jobs

EXTRACTOR_REGISTRY = {
    # existing extractors…
    "stripe": extract_stripe_jobs,
}
