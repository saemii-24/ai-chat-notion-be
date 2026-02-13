from fastapi import FastAPI
from app.ask.router import router as ask_router
from dotenv import load_dotenv

load_dotenv()


app = FastAPI()

app.include_router(ask_router, prefix="/ask", tags=["Ask"])
app.include_router(ask_router, prefix="/modify", tags=["Modify"])
