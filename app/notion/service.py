import os
from typing import Any, Dict, List
from notion_client import Client

# =========================
# Notion Client & DB IDs
# =========================


# =========================
# WORD
# =========================


def create_word_page(props: Dict[str, Any]):
    """
    WORD DB:
    - 영어 표현 (title)
    - 한국어 뜻 (rich_text)
    - 영어 예문 (rich_text)
    """
    notion = Client(auth=os.environ["NOTION_API_KEY"])
    WORD_DB_ID = os.environ["WORD_DB_ID"]

    return notion.pages.create(
        parent={"database_id": WORD_DB_ID},
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


# =========================
# SENTENCE
# =========================


def create_sentence_page(props: Dict[str, Any]):
    """
    SENTENCE DB:
    - 한국어 문장 (title)
    - 영어 표현 (rich_text)
    - 사용 상황 (rich_text)
    - 변형 예문 (rich_text)
    """
    notion = Client(auth=os.environ["NOTION_API_KEY"])
    SENTENCE_DB_ID = os.environ["SENTENCE_DB_ID"]
    return notion.pages.create(
        parent={"database_id": SENTENCE_DB_ID},
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


# =========================
# GRAMMAR
# =========================


def create_grammar_page(
    title: str,
    category: str,
    children: List[Dict[str, Any]],
):
    """
    GRAMMAR DB:
    - 제목 (title)
    - 분류 (select)
    - 본문은 children (Markdown → blocks)
    """
    notion = Client(auth=os.environ["NOTION_API_KEY"])
    GRAMMAR_DB_ID = os.environ["GRAMMAR_DB_ID"]
    return notion.pages.create(
        parent={"database_id": GRAMMAR_DB_ID},
        properties={
            "제목": {"title": [{"text": {"content": title}}]},
            "분류": {"select": {"name": category}},
        },
        children=children,
    )


# =========================
# Markdown → Notion Children
# =========================


def markdown_to_children(markdown: str) -> List[Dict[str, Any]]:
    """
    최소 문법 지원:
    - #  → heading_1
    - ## → heading_2
    - -  → bulleted_list_item
    - 그 외 → paragraph
    """
    children: List[Dict[str, Any]] = []

    for raw_line in markdown.splitlines():
        line = raw_line.strip()

        if not line:
            continue

        if line.startswith("# "):
            children.append(
                {
                    "type": "heading_1",
                    "heading_1": {"rich_text": [{"text": {"content": line[2:]}}]},
                }
            )

        elif line.startswith("## "):
            children.append(
                {
                    "type": "heading_2",
                    "heading_2": {"rich_text": [{"text": {"content": line[3:]}}]},
                }
            )

        elif line.startswith("- "):
            children.append(
                {
                    "type": "bulleted_list_item",
                    "bulleted_list_item": {
                        "rich_text": [{"text": {"content": line[2:]}}]
                    },
                }
            )

        else:
            children.append(
                {
                    "type": "paragraph",
                    "paragraph": {"rich_text": [{"text": {"content": line}}]},
                }
            )

    return children


# =========================
# Dispatcher (연결 핵심)
# =========================


def save_result_to_notion(result: Dict[str, Any]):
    """
    Gemini 결과를 받아
    TYPE에 따라 알맞은 DB에 저장한다.
    """
    result_type = result["type"]

    if result_type == "WORD":
        return create_word_page(result["properties"])

    elif result_type == "SENTENCE":
        return create_sentence_page(result["properties"])

    elif result_type == "GRAMMAR":
        children = markdown_to_children(result["markdown"])
        return create_grammar_page(
            title=result["properties"]["제목"],
            category=result["properties"]["분류"],
            children=children,
        )

    else:
        raise ValueError(f"Unknown result type: {result_type}")
