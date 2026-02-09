FROM python:3.12-slim

WORKDIR /app

ENV PYTHONPATH=/app

# 安裝系統依賴 (包含 bcrypt 需要的)
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# 安裝 Python 依賴
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 複製原始碼
COPY . .

# 預設啟動指令 (會被 docker-compose 覆蓋)
CMD ["sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"]
