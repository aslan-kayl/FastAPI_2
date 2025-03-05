from typing import Optional
from sqlmodel import select
from .schemas import UserCreateModel
from src.con.models import User
from sqlmodel.ext.asyncio.session import AsyncSession
from src.auth.converters import convert_user_create_to_orm
from .utils import generate_passwd_hash


class UserService:
    async def get_user_by_phone(self, phone: str, session: AsyncSession) -> Optional[User]:
        statement = select(User).where(User.phone == phone)

        result = await session.exec(statement)

        return result.first()

    async def user_exists(self, phone: str, session: AsyncSession) -> bool:
        user = await self.get_user_by_phone(phone, session)

        return True if user is not None else False

    async def create_user(self, user_data: UserCreateModel, session: AsyncSession) -> User:
        data = user_data.model_dump()
        new_user = User(**data)
        new_user.password_hash = generate_passwd_hash(data['password'])
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)

        return new_user

