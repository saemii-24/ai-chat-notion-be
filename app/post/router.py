from fastapi import APIRouter, Depends
from app.post.schemas import PostCreate
from app.auth.service import get_current_user 

router = APIRouter()

@router.post("/post")
async def create_post(
    payload: PostCreate,
    current_user: str = Depends(get_current_user),  # 현재 로그인한 유저 정보 가져오기
):

    new_post = {
        "id": 1,
        "title": payload.title,
        "content": payload.content,
        "author_id": payload.author_id,
        "author": current_user, 
    }

    return {"message": "Post created successfully", "post": new_post}
