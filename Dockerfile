FROM python:3.11-slim

# OCR 엔진 설치
RUN apt-get update && \
    apt-get install -y tesseract-ocr tesseract-ocr-kor && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# 작업 디렉토리
WORKDIR /app

# uv 설치
RUN pip install --no-cache-dir uv

# 의존성 먼저 복사 
COPY pyproject.toml uv.lock ./
RUN uv sync --no-dev

# 소스 코드 복사
COPY . .

# FastAPI 실행
CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

