from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import redis
from app.dependencies import get_user_by_id, confirm_temp_user
from app.schemas import UserCreate, UserView, UserChange, TempUserData
from app.utils import generate_verification_code, hash_password
from app.database import get_scoped_session
from app.services.email_sender import send_verification_code
from app.services.sms_sender import send_sms
from app.crud import CRUD_User


router = APIRouter()


@router.post('/users/', status_code=status.HTTP_202_ACCEPTED)
async def new_user_registration(
    user_create: UserCreate,
    async_session: Annotated[AsyncSession, Depends(get_scoped_session)]
) -> TempUserData:
    user_exist = await CRUD_User(async_session).read(
        email=user_create.email, phone_number=user_create.phone_number)
    if user_exist:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='This user exist'
        )

    code = generate_verification_code()
    if user_create.email:
        # await send_verification_code(user.email, code)
        print(f'--> send_email(user.phone_number, code')

    elif user_create.phone_number:
        print(f'--> send_sms(user.phone_number, code')

    # Save to Redis
    key = f'pending_user:{user_create.email or user_create.phone_number}'
    user_dict = user_create.model_dump(exclude_none=True)
    user_dict['code'] = code
    await redis.hset(key, mapping=user_dict)
    await redis.expire(key, time=3600)
    return TempUserData(key=key, code=code)


@router.post('/users/confirm-code', status_code=status.HTTP_201_CREATED)
async def code_confirmation(
    temp_user_data: TempUserData,
    session: Annotated[AsyncSession, Depends(get_scoped_session)]
) -> UserView:
    user_create = await confirm_temp_user(temp_user_data)
    user_create.password = hash_password(user_create.password)
    user_model = await CRUD_User(session).create(user_create.model_dump())
    return UserView.model_validate(user_model)


@router.get('/users/{user_id}/')
async def show_user(
    user: Annotated[UserView, Depends(get_user_by_id)]
) -> UserView:
    return user


@router.patch('/users/{user_id}/')
async def change_user(
    user_change: UserChange,
    user: Annotated[UserView, Depends(get_user_by_id)],
    async_session: Annotated[AsyncSession, Depends(get_scoped_session)]
) -> UserView:
    changed_data = user_change.model_dump(exclude_unset=True, exclude_defaults=True)
    user_model = await CRUD_User(async_session).update(user.id, changed_data)
    return UserView.model_validate(user_model)


@router.delete('/users/{user_id}/', status_code=status.HTTP_204_NO_CONTENT)
async def remove_user(
    user: Annotated[UserView, Depends(get_user_by_id)],
    async_session: Annotated[AsyncSession, Depends(get_scoped_session)]
) -> None:
    await CRUD_User(async_session).delete(user.id)
