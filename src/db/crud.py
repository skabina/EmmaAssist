from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from .models import User

class UserCRUD:
    async def get_user_by_tg_id(self, session: AsyncSession,  telegram_id: int) -> User | None:
        user = await session.scalars(
            select(User).where(User.telegram_id ==  telegram_id)
        )
        
        return user.one_or_none()


    async def create_user(self, session: AsyncSession, telegram_id: int, email: str, app_password: str) -> User:
        user = User(telegram_id=telegram_id, email=email, app_password=app_password)
        user = await session.merge(user)
        await session.commit()
        return user

    
crud = UserCRUD()