import json
import re
from google import genai

from app.llm.prompt import build_notion_ready_prompt, modify_presence_markdown


def ask_gemini(question: str) -> dict:
    """
    1. 프롬프트 생성
    2. Gemini 호출
    3. JSON 파싱
    4. dict 반환
    """
    client = genai.Client()
    prompt = build_notion_ready_prompt(question)

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )

    print(response)

    raw = response.text.strip()

    if raw.startswith("```"):
        raw = re.sub(r"^```json\s*|\s*```$", "", raw, flags=re.DOTALL)

    try:
        return json.loads(raw)
    except json.JSONDecodeError as e:
        print("🔥 Gemini raw output (NOT JSON):")
        print(raw)
        raise e


def ask_gemini_modify(location: str) -> str:
    client = genai.Client()
    prompt = modify_presence_markdown(location)

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )

    raw = response.text.strip()

    if raw.startswith("```"):
        raw = re.sub(r"^```(?:markdown)?\s*|\s*```$", "", raw, flags=re.DOTALL)

    return raw
