from fastapi import APIRouter, Depends, HTTPException
from requests import Session
from app import db
from app.auth.models import User
from app.deps import get_db
from app.post.models import Post, TopPost
from app.post.schemas import PostCreate, PostDetail, PostList
from app.auth.service import get_current_user
from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.post("/create")
async def create_post(
    payload: PostCreate,  # 프론트에서 보내는 코드
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    new_post = Post(  # Post 테이블을 지정해줌
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


@router.get("/top/latest")
async def get_latest_top_post(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(TopPost).order_by(desc(TopPost.picked_at)).limit(1)
    )
    latest = result.scalar_one_or_none()

    if latest is None:
        return {"message": "No top post yet"}

    return {
        "id": latest.id,
        "post_id": latest.post_id,
        "picked_at": latest.picked_at,
    }

@router.get("/{post_id}", response_model=PostDetail)
async def get_post_by_id(
    post_id: int,
    db: Session = Depends(get_db),
):
    """
    id 값으로 게시글을 상세 조회한다.
    """
    post = db.query(Post).filter(Post.id == post_id).first()

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    return post