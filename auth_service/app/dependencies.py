from typing import Annotated

import jwt
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status

from app.services.jwt_manager import verify_token
from app.database import get_scoped_session
from app.schemas import UserView, UserCreate, TempUserData, FullUserInfo
from app.config import redis
from app.crud import CRUD_User


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


async def get_me(
    async_session: Annotated[AsyncSession, Depends(get_scoped_session)],
    token: Annotated[str, Depends(oauth2_scheme)]
) -> FullUserInfo:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = verify_token(token)
        user_id = payload.get('sub')
        if user_id is None:
            raise credentials_exception

    except jwt.exceptions.PyJWTError:
        raise credentials_exception

    user = await CRUD_User(async_session).read(user_id=user_id)
    if user is None:
        raise credentials_exception
    
    user_dict = UserView.model_validate(user).model_dump()
    user_dict.update({
            'logged_in_at': payload.get('iat'),
            'expires': payload.get('exp')
        })
    return FullUserInfo(**user_dict)


async def get_user_by_id(
        user_id: int,
        async_session: AsyncSession = Depends(get_scoped_session),
) -> UserView:
    user = await CRUD_User(async_session).read(user_id=user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found.'
        )

    user_base = UserView.model_validate(user)
    return user_base


async def confirm_temp_user(temp_user: TempUserData) -> UserCreate:
    pending_user_exception = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail='Invalid code.'
    )
    pending_user_data: dict = await redis.hgetall(temp_user.key)
    if pending_user_data is None:
        raise pending_user_exception

    correct_code = pending_user_data.pop('code')
    if correct_code != str(temp_user.code):
        raise pending_user_exception

    await redis.delete(temp_user.key)
    user_base = UserCreate.model_validate(pending_user_data)
    return user_base
