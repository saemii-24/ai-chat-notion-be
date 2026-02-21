from fastapi import FastAPI
from dotenv import load_dotenv

from app.ask.router import router as ask_router
from app.modify.router import router as modify_router
from app.auth.router import router as auth_router
from app.post.router import router as post_router

from app.db.db import engine, Base
from app.auth import models

load_dotenv()

app = FastAPI()

# DB 테이블 생성
Base.metadata.create_all(bind=engine)

# 라우터 등록
app.include_router(ask_router, prefix="/ask", tags=["Ask"])
app.include_router(modify_router, prefix="/modify", tags=["Modify"])
app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(post_router, prefix="/post", tags=["Post"])
