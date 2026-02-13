from fastapi import APIRouter
from app.modify.models import ModifyRequest
from app.llm.service import ask_gemini_modify
from app.notion.service import save_result_to_notion

router = APIRouter()


@router.post("/modify")
async def modify_note(payload: ModifyRequest):

    # 사용자가 한 번에 여러 종류의 여러 질문을 물어볼 수 있음
    results = ask_gemini_modify(payload.location)
    for result in results:
        save_result_to_notion(result)

    return {
        "request_notion_id": payload.location,
        "saved": True,
    }
