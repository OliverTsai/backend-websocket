from fastapi import APIRouter
from app.api.v1 import auth

api_router = APIRouter()

api_router.include_router(auth.router)
# 後續加入其他路由:
# api_router.include_router(users.router)
# api_router.include_router(friends.router)
# api_router.include_router(rooms.router)
# api_router.include_router(messages.router)
