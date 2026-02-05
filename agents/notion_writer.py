import os
from notion_client import Client
from dotenv import load_dotenv
from datetime import date

load_dotenv()

notion = Client(auth=os.getenv("NOTION_TOKEN"))
DATA_SOURCE_ID = os.getenv("NOTION_DATABASE_ID")


def write_job_to_notion(job: dict):
    """
    job dict expected keys (minimal):
    - position
    - company
    - posting_url

    optional:
    - place
    - country
    - remote
    - industry
    - stage
    - applied_date
    - keywords
    - required_skills
    - required_years
    - fit_score
    - job_description
    - motivation_text
    - kontakt
    - kontakt_linkedin
    """

    properties = {
        "Position": {
            "title": [{"text": {"content": job["position"]}}]
        },
        "Company": {
            "rich_text": [{"text": {"content": job["company"]}}]
        },
        "Posting URL": {
            "url": job["posting_url"]
        },
        "Stage": {
            "status": {"name": job.get("stage", "Found")}
        },
        "Applied": {
            "date": {
                "start": job.get(
                    "applied_date",
                    date.today().isoformat()
                )
            }
        }
    }

    # Optional fields (only added if present)
    if job.get("place"):
        properties["Place"] = {
            "rich_text": [{"text": {"content": job["place"]}}]
        }

    if job.get("country"):
        properties["Country"] = {
            "select": {"name": job["country"]}
        }

    if job.get("remote"):
        properties["Remote"] = {
            "select": {"name": job["remote"]}
        }

    if job.get("industry"):
        properties["Industry"] = {
            "select": {"name": job["industry"]}
        }

    if job.get("keywords"):
        properties["Keywords"] = {
            "multi_select": [{"name": k} for k in job["keywords"]]
        }

    if job.get("required_skills"):
        properties["Required skills"] = {
            "multi_select": [{"name": s} for s in job["required_skills"]]
        }

    if job.get("required_years") is not None:
        properties["Required years"] = {
            "number": job["required_years"]
        }

    if job.get("fit_score") is not None:
        properties["Fit score"] = {
            "number": job["fit_score"]
        }

    if job.get("job_description"):
        properties["Job Description"] = {
            "rich_text": [{"text": {"content": job["job_description"]}}]
        }

    if job.get("motivation_text"):
        properties["Motivation text"] = {
            "rich_text": [{"text": {"content": job["motivation_text"]}}]
        }

    if job.get("kontakt"):
        properties["Kontakt"] = {
            "rich_text": [{"text": {"content": job["kontakt"]}}]
        }

    if job.get("kontakt_linkedin"):
        properties["Kontakt LinkedIn"] = {
            "url": job["kontakt_linkedin"]
        }

    notion.pages.create(
        parent={"data_source_id": DATA_SOURCE_ID},
        properties=properties
    )
