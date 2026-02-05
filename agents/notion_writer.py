import os
from notion_client import Client
from dotenv import load_dotenv

load_dotenv()

notion = Client(auth=os.getenv("NOTION_TOKEN"))
DATABASE_ID = os.getenv("NOTION_DATABASE_ID")


def save_to_notion(job):
    notion.pages.create(
        parent={"database_id": DATABASE_ID},
        properties={
            "Company": {
                "title": [{"text": {"content": job["company"]}}]
            },
            "Role": {
                "rich_text": [{"text": {"content": job["role"]}}]
            },
            "Job URL": {
                "url": job["job_url"]
            },
            "Status": {
                "select": {"name": "Found"}
            },
            "Fit Score": {
                "number": job.get("score", 0)
            }
        }
    )
