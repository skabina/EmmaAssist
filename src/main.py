import asyncio

from aiogram import BaseMiddleware, Bot, Dispatcher

from .database import db_helper 
from .config import settings
from .handlers.handler import router



dp = Dispatcher()
dp.include_router(router)

class DatabaseMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        async with db_helper.session_dependency() as session:
            data['session'] = session
            return await handler(event, data)

dp.message.middleware(DatabaseMiddleware())


async def main() -> None:
    bot = Bot(token=settings.env.BOT_TOKEN)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
          