from fastapi import FastAPI
from app.ocr.router import router as ocr_router

app = FastAPI()

app.include_router(ocr_router, prefix="/ocr", tags=["OCR"])
