from fastapi import APIRouter
from app.ask.models import QuestionRequest
from app.llm.service import ask_gemini
from app.notion.service import save_result_to_notion

router = APIRouter()


@router.post("/ask")
async def ask_question(payload: QuestionRequest):
    result = ask_gemini(payload.question)

    save_result_to_notion(result)

    return {
        "question": payload.question,
        "type": result["type"],
        "saved": True,
    }
