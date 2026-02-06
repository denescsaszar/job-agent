def extract_stripe_jobs(data: dict) -> list[dict]:
    jobs = []

    # Stripe structure: data["jobs"] is a list of roles
    for job in data.get("jobs", []):
        jobs.append({
            "source": "stripe",
            "title": job.get("title"),
            "location": ", ".join(job.get("locations", [])),
            "team": job.get("team"),
            "url": f"https://stripe.com/jobs/{job.get('slug')}",
        })

    return jobs
