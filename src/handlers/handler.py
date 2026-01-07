from aiogram import Router, types
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from sqlalchemy.ext.asyncio import AsyncSession

from ..db.crud import crud


router = Router()


class RegStates(StatesGroup):
    waiting_email = State()
    waiting_password = State()


@router.message(CommandStart())
async def start_handler(message: types.Message, session: AsyncSession):

    telegram_id = message.from_user.id
    
    user = await crud.get_user_by_tg_id(session, telegram_id)

    if user:
        await message.answer(f"З поверненням, {user.email}!")
    else:
        await message.answer("Вітаю! Використовуйте /register для реєстрації.")


@router.message(Command("register"))
async def register_start(message: types.Message, state: FSMContext):
    await message.answer("Введіть ваш email:")
    await state.set_state(RegStates.waiting_email)


@router.message(RegStates.waiting_email)
async def process_email(message: types.Message, state: FSMContext):
    email = message.text
    await state.update_data(email=email)
    await message.answer("Введіть ваш пароль додатка:")
    await state.set_state(RegStates.waiting_password)


@router.message(RegStates.waiting_password)
async def process_password(message: types.Message, state: FSMContext, session: AsyncSession):
    password = message.text
    data = await state.get_data()
    email = data['email']
    telegram_id = message.from_user.id

    await crud.create_user(session, telegram_id, email, password)
    await message.answer("Привіт! Ти успішно зареєстрований в системі.")
    await state.clear()
