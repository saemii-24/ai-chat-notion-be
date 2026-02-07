from google import genai

client = genai.Client()


def build_notion_ready_prompt(ocr_text: str) -> str:
    return f"""
너는 OCR로 추출된 텍스트를
사람이 노션에 정리하기 쉽게 다듬어주는 역할이야.

아래 텍스트는 이미지에서 추출된 OCR 결과라
오타, 줄바꿈 오류, 중복, 의미 없는 문자열이 있을 수 있어.

이 텍스트를 읽고,
노션에 바로 정리해서 쓰기 좋은 형태로 Markdown으로 정리해줘.

요구사항:
- 반드시 Markdown 형식으로 작성
- 과도한 재해석이나 상상은 하지 말 것
- 원문 내용을 최대한 보존하되, 읽기 좋게만 정리
- 설명 문장은 쓰지 말고, 결과만 출력

구조:
# 제목 (내용을 대표하는 한 줄)

## 요약
- 핵심 내용 3~5줄

## 정리된 내용
- 문단 단위로 자연스럽게 정리
- 필요하면 목록(-) 사용
- 필요하면 테이블 사용

OCR 원문:
{ocr_text}
"""


def format_ocr_text_for_notion(ocr_text: str) -> str:
    prompt = build_notion_ready_prompt(ocr_text)

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )

    return response.text
