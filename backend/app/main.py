from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import socketio

from app.config import settings
from app.api.v1.router import api_router
from app.socket.manager import sio

# 建立 FastAPI 應用
app = FastAPI(
    title="Chat API",
    description="即時聊天系統 API",
    version="1.0.0",
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
)

# CORS 設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 正式環境請限制
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 掛載 REST API 路由
app.include_router(api_router)

# 整合 Socket.IO
socket_app = socketio.ASGIApp(sio, other_asgi_app=app)


# Health check
@app.get("/health")
async def health_check():
    return {"status": "ok"}


# 用 socket_app 作為最終的 ASGI 應用
app = socket_app
