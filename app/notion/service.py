import os
from typing import Any, Dict, List
from notion_client import Client

notion = Client(auth=os.environ["NOTION_API_KEY"])


def create_word_page(database_id: str, props: Dict[str, Any]):
    return notion.pages.create(
        parent={"database_id": database_id},
        properties={
            "영어 표현": {"title": [{"text": {"content": props["영어 표현"]}}]},
            "한국어 뜻": {"rich_text": [{"text": {"content": props["한국어 뜻"]}}]},
            "영어 예문": {
                "rich_text": [
                    {"text": {"content": e + "\n"}} for e in props["영어 예문"]
                ]
            },
        },
    )


def create_sentence_page(database_id: str, props: Dict[str, Any]):
    return notion.pages.create(
        parent={"database_id": database_id},
        properties={
            "한국어 문장": {"title": [{"text": {"content": props["한국어 문장"]}}]},
            "영어 표현": {"rich_text": [{"text": {"content": props["영어 표현"]}}]},
            "사용 상황": {"rich_text": [{"text": {"content": props["사용 상황"]}}]},
            "변형 예문": {
                "rich_text": [
                    {"text": {"content": e + "\n"}} for e in props["변형 예문"]
                ]
            },
        },
    )


def create_grammar_page(
    database_id: str,
    title: str,
    category: str,
    children: List[Dict[str, Any]],
):
    return notion.pages.create(
        parent={"database_id": database_id},
        properties={
            "제목": {"title": [{"text": {"content": title}}]},
            "분류": {"select": {"name": category}},
        },
        children=children,
    )
