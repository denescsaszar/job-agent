def extract_stripe_jobs(data: dict) -> list[dict]:
    jobs = []

    try:
        job_nodes = data["props"]["pageProps"].get("jobs", [])
    except Exception:
        print("[stripe] ❌ Unexpected JSON structure")
        return []

    for job in job_nodes:
        jobs.append({
            "position": job.get("title"),
            "company": "Stripe",
            "place": job.get("location"),
            "posting_url": f"https://stripe.com/jobs/listing/{job.get('slug')}",
            "source": "stripe",
        })

    return jobs
