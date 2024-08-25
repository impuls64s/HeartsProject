from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    async_scoped_session
)

from app.models import User


class CRUD_User:
    def __init__(
            self,
            async_session: async_scoped_session[AsyncSession]
    ) -> None:
        self.async_session = async_session

    async def create(self, user_dict: dict) -> User:
        new_user = User(**user_dict)
        self.async_session.add(new_user)
        await self.async_session.commit()
        return new_user

    async def read(
            self,
            user_id: Optional[int] = None,
            email: Optional[str] = None,
            phone_number: Optional[str] = None
    ) -> User:
        if not any([user_id, email, phone_number]):
            raise ValueError(
                'Either user_id, email, or phone_number must be provided'
            )

        query = select(User)
        if user_id:
            query = query.filter(User.id==user_id)
        elif email:
            query = query.filter(User.email==email)
        elif phone_number:
            query = query.filter(User.phone_number==phone_number)

        result = await self.async_session.execute(query)
        user = result.scalars().first()
        return user

    async def update(self, user_id: int, data: dict) -> User:
        query = select(User).filter(User.id==user_id)
        result = await self.async_session.execute(query)
        user = result.scalars().first()
        for name, value in data.items():
            setattr(user, name, value)
        await self.async_session.commit()
        return user

    async def delete(self, user_id: int) -> None:
        query = select(User).filter(User.id==user_id)
        result = await self.async_session.execute(query)
        user = result.scalars().first()
        await self.async_session.delete(user)
        await self.async_session.commit()

