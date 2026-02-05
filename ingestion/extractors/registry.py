from ingestion.extractors.stripe import extract_stripe_jobs

EXTRACTOR_REGISTRY = {
    "extract_stripe_jobs": extract_stripe_jobs,
}
