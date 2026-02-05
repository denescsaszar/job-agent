from agents.job_ingestion import run_ingestion


def main():
    jobs = run_ingestion()

    print("\n=== INGESTED JOBS ===")
    for job in jobs:
        print(f"- {job['position']} | {job['company']} | {job['country']}")


if __name__ == "__main__":
    main()
