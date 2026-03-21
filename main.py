from contextlib import asynccontextmanager

from fastapi import FastAPI
from dotenv import load_dotenv

from app.ask.router import router as ask_router
from app.modify.router import router as modify_router
from app.auth.router import router as auth_router
from app.post.router import router as post_router

from app.db.db import engine, Base
from app.auth import models
from app.post import models as post_models
from app.scheduler.scheduler import scheduler, register_jobs

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # DB table creation
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # scheduler setup
    register_jobs()
    scheduler.start()
    print("scheduler started")

    yield

    # shutdown
    scheduler.shutdown()
    print("scheduler stopped")


app = FastAPI(lifespan=lifespan)

# router registration
app.include_router(ask_router, prefix="/ask", tags=["Ask"])
app.include_router(modify_router, prefix="/modify", tags=["Modify"])
app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(post_router, prefix="/post", tags=["Post"])
