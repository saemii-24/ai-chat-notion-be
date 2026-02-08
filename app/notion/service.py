from notion_client import Client
import os

notion = Client(auth=os.environ["NOTION_API_KEY"])


def create_notion_page(database_id: str, title: str, children: list):
    return notion.pages.create(
        parent={"database_id": database_id},
        properties={"제목": {"title": [{"text": {"content": title}}]}},
        children=children,
    )
