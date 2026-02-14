from fastapi import APIRouter

router = APIRouter()


@router.get("/today")
async def today_word():

   
