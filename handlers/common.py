from aiogram import F, Router
from aiogram.filters import Command
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message

from keyboards.client_kb import kb_client_delivery

router = Router()


@router.message(Command(commands=["start"]))
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(text="Для подтверждения доставки - введите команду /delivery")


@router.message(StateFilter(None), Command(commands=["cancel"]))
@router.message(default_state, F.text.lower() == "отмена")
async def cmd_cancel_no_state(message: Message, state: FSMContext):
    await state.set_data({})
    await message.answer(
        text="Нечего отменять",
        reply_markup=kb_client_delivery()
    )


@router.message(StateFilter(None), Command(commands=["help"]))
@router.message(default_state, F.text.lower() == "help")
async def cmd_help(message: Message, state: FSMContext):
    await state.set_data({})
    await message.answer(
        text="Команда /delivery - для подтверждения доставки.\nЛибо кнопка 'загрузить'",
        reply_markup=kb_client_delivery()
    )


@router.message(Command(commands=["cancel"]))
@router.message(F.text.lower() == "отмена")
async def cmd_cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text="Действие отменено",
        reply_markup=kb_client_delivery()
    )
