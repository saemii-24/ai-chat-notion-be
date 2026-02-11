from fastapi import APIRouter
from app.ask.models import QuestionRequest
from app.llm.service import ask_gemini
from app.notion.service import save_result_to_notion

router = APIRouter()


@router.post("/ask")
async def ask_question(payload: QuestionRequest):

    # 사용자가 한 번에 여러 종류의 여러 질문을 물어볼 수 있음
    results = ask_gemini(payload.question)

    for result in results:
        save_result_to_notion(result)

    return {
        "question": payload.question,
        "type": result["type"],
        "saved": True,
    }
