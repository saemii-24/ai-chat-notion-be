from fastapi import APIRouter, UploadFile, File
from fastapi.concurrency import run_in_threadpool

from app.ocr.service import extract_text_from_image
from app.llm.service import format_ocr_text_for_notion

router = APIRouter()


@router.post("/")
async def ocr_image(file: UploadFile = File(...)):
    # 1. OCR (CPU-bound → threadpool)
    ocr_text = await run_in_threadpool(extract_text_from_image, file)

    # 2. Gemini (네트워크 I/O → async 안 막힘)
    notion_markdown = format_ocr_text_for_notion(ocr_text)

    return {
        "filename": file.filename,
        "ocr_text": ocr_text,
        "notion_ready": notion_markdown,
    }
