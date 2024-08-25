from typing import Annotated

import jwt
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_scoped_session
from app.schemas import JWToken, RefreshTokenRequest, UserView, FullUserInfo
from app.utils import authenticate_user
from app.dependencies import get_me
from app.services.jwt_manager import (
    create_access_token,
    create_refresh_token,
    refresh_access_token,
    InvalidTokenTypeError
)


router = APIRouter()


@router.get('/users/me/', response_model=FullUserInfo)
async def read_users_me(
    user: Annotated[FullUserInfo, Depends(get_me)],
) -> FullUserInfo:
    return user


@router.post('/token')
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: Annotated[AsyncSession, Depends(get_scoped_session)],
) -> JWToken:
    user = await authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    payload = {'sub': user.id, 'name': user.name}
    access_token = create_access_token(payload)
    refresh_token = create_refresh_token(payload)
    return JWToken(access_token=access_token, refresh_token=refresh_token)


@router.post('/token/refresh')
async def generate_new_access_token(token: RefreshTokenRequest) -> JWToken:
    try:
        new_access_token = refresh_access_token(token.refresh_token)
    except (jwt.exceptions.PyJWTError, InvalidTokenTypeError) as error:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid refresh token. Exception: {error}",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return JWToken(access_token=new_access_token, refresh_token=token.refresh_token)
