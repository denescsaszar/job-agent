import os
from notion_client import Client
from dotenv import load_dotenv

load_dotenv()

notion = Client(auth=os.getenv("NOTION_TOKEN"))
DATABASE_ID = os.getenv("NOTION_DATABASE_ID")

EXPECTED_PROPERTIES = {
    "Position": "title",
    "Company": "rich_text",
    "Place": "rich_text",
    "Country": "select",
    "Remote": "select",
    "Industry": "select",
    "Stage": "status",
    "Posting URL": "url",
    "Applied": "date",
    "Keywords": "multi_select",
    "Required skills": "multi_select",
    "Required years": "number",
    "Fit score": "number",
    "Job Description": "rich_text",
    "CV Version (PDF)": "files",
    "Motivation text": "rich_text",
    "Motivation PDF": "files",
    "Kontakt": "rich_text",
    "Kontakt LinkedIn": "url",
}

db = notion.data_sources.retrieve(data_source_id=DATABASE_ID)

print(db.keys())

properties = db["properties"]

errors = []

for name, expected_type in EXPECTED_PROPERTIES.items():
    if name not in properties:
        errors.append(f"❌ Missing property: {name}")
    else:
        actual_type = properties[name]["type"]
        if actual_type != expected_type:
            errors.append(
                f"⚠️ Property '{name}' has type '{actual_type}' (expected '{expected_type}')"
            )

if errors:
    print("\nSchema issues found:\n")
    for e in errors:
        print(e)
else:
    print("✅ Notion schema matches expected structure")
