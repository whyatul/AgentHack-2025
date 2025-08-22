# Python slim base
FROM python:3.11-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# System deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential curl git && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./src ./src
COPY README.md .

EXPOSE 8000

# Default command (overrideable)
CMD ["uvicorn", "src.ai_meme_stock_predictor.web.app:app", "--host", "0.0.0.0", "--port", "8000"]
