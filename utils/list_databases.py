import os
from notion_client import Client
from dotenv import load_dotenv

load_dotenv()

notion = Client(auth=os.getenv("NOTION_TOKEN"))

results = notion.search(
    filter={"property": "object", "value": "data_source"}
)

for db in results["results"]:
    title = "Untitled"
    if db.get("title"):
        title = db["title"][0]["plain_text"]

    print("Title:", title)
    print("ID:   ", db["id"])
    print("URL:  ", db.get("url"))
    print("-" * 40)
