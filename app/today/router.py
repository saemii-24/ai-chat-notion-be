from fastapi import APIRouter
from app.notion.word_service import get_random_words

router = APIRouter()


@router.get("/today")
async def today_word():
    words = get_random_words(5)
    return {"today_words": words}
