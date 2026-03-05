from fastapi import APIRouter, Depends
from requests import Session
from app import db
from app.auth.models import User
from app.deps import get_db
from app.post.models import Post
from app.post.schemas import PostCreate, PostList
from app.auth.service import get_current_user 

router = APIRouter()

@router.post("/create")
async def create_post(
    payload: PostCreate, #프론트에서 보내는 코드
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    new_post = Post( #Post 테이블을 지정해줌
        title=payload.title,
        content=payload.content,
        author_id=current_user.id,
    )

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return {
        "message": "Post created successfully",
        "post": new_post,
    }

@router.get("/posts", response_model=list[PostList])
async def get_posts(db: Session = Depends(get_db)):
    """
    전체 게시글 목록 조회

    DB에서 모든 게시글(Post)을 조회하여
    PostList 스키마 형태의 리스트로 반환한다.
    """
    posts = db.query(Post).all()
    return posts

@router.get("/posts/me", response_model=list[PostList])
async def get_my_posts(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    현재 로그인한 사용자의 게시글 목록 조회

    JWT 토큰을 통해 인증된 current_user의 id를 기준으로
    해당 사용자가 작성한 게시글만 조회한다.
    """
    posts = db.query(Post).filter(Post.author_id == current_user.id).all()
    return posts