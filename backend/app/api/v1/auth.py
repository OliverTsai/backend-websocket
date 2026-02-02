from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.schemas.auth import RegisterRequest, LoginRequest, TokenResponse, UserResponse
from app.services.auth import AuthService, create_access_token

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=UserResponse)
async def register(
    data: RegisterRequest,
    session: AsyncSession = Depends(get_db)
):
    """註冊新用戶"""
    user = await AuthService.register(session, data)
    return user


@router.post("/login", response_model=TokenResponse)
async def login(
    data: LoginRequest,
    session: AsyncSession = Depends(get_db)
):
    """用戶登入"""
    user = await AuthService.login(session, data.email, data.password)
    access_token = create_access_token(user.id)
    return TokenResponse(access_token=access_token)
