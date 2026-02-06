from fastapi import APIRouter, UploadFile, File
from app.ocr.service import extract_text_from_image

router = APIRouter()


@router.post("/")
async def ocr_image(file: UploadFile = File(...)):
    text = extract_text_from_image(file)
    return {"filename": file.filename, "text": text}
