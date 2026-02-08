from fastapi import APIRouter
from app.ask.models import QuestionRequest
from app.llm.service import format_question_for_notion

router = APIRouter()


@router.post("/ask")
async def ask_question(payload: QuestionRequest):
    """
    사용자 질문을 받아서
    - Gemini 호출
    - WORD / GRAMMAR / SENTENCE 판별
    - Notion 저장
    - 결과 반환
    """
    result = format_question_for_notion(payload.question)

    return {
        "question": payload.question,
        "type": result["type"],
        "markdown": result["markdown"],
    }
