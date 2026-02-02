import socketio
from app.config import settings

# 建立 AsyncServer
sio = socketio.AsyncServer(
    async_mode="asgi",
    cors_allowed_origins="*",  # 正式環境請限制
    logger=settings.DEBUG,
    engineio_logger=settings.DEBUG,
)
