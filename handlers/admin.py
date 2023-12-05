import os

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State, default_state

from aiogram.types import Message, ReplyKeyboardRemove

from filters.filter_admin import AdminFilter

from keyboards.admin_kb import kb_yes_cancel
from keyboards.client_kb import kb_client_delivery

router = Router()


class ChangePathsToSave(StatesGroup):
    change_path_to_save = State()
    input_path_to_save = State()


class ChangePathsToExcel(StatesGroup):
    change_path_to_excel = State()
    input_path_to_excel = State()


@router.message(StateFilter(None), Command(commands=["help"]), AdminFilter(is_admin=True))
@router.message(default_state, F.text.lower() == "help", AdminFilter(is_admin=True))
async def cmd_admin_help(message: Message, state: FSMContext):
    await state.set_data({})
    await message.answer(
        text="Команда /delivery - для подтверждения доставки.\nЛибо кнопка 'загрузить'\n\n"
             "/path_to_save - команда, для изменения пути сохранения файла\n\n"
             "/path_to_excel - команда, для изменения пути по которому лежит файл excel id-адресов\n\n"
             "/create - команда, для создания файлов, хранящих все пути\n\n",

        reply_markup=kb_client_delivery()
    )


@router.message(Command(commands=["path_to_save"]), AdminFilter(is_admin=True))
async def cmd_path_to_save(message: Message, state: FSMContext):
    try:
        with open("data/path_to_save.txt", encoding="utf-8") as file:
            path_to_save = file.read()

        await message.answer(
            text=f"Текущий путь сохранения\n<b>{path_to_save}</b>\nХотите изменить???", reply_markup=kb_yes_cancel()
        )
        await state.set_state(ChangePathsToSave.change_path_to_save)
    except Exception:
        await message.answer(
            text="Файл хранения данных отсутствует.\n"
                 "Введите команду /create"
        )


@router.message(ChangePathsToSave.change_path_to_save, F.text.lower() == "да")
async def change_path_to_save(message: Message, state: FSMContext):
    await message.answer(
        text="Введите путь к папке сохранения"
             "\nв формате\n<b>папка1/папка2/</b>",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(ChangePathsToSave.input_path_to_save)


@router.message(ChangePathsToSave.input_path_to_save, F.text)
async def input_path_to_save(message: Message, state: FSMContext):
    path_to_save = message.text
    with open("data/path_to_save.txt", "w", encoding="utf-8") as file:
        file.write(path_to_save)

    await state.clear()
    await message.answer(text=f"Готово!!!\nНовый путь сохранения\n<b>{path_to_save}</b>")


@router.message(Command(commands=["path_to_excel"]), AdminFilter(is_admin=True))
async def cmd_path_to_excel(message: Message, state: FSMContext):
    try:
        with open("data/path_to_excel.txt", encoding="utf-8") as file:
            path_to_excel = file.read()

        await message.answer(
            text=f"Текущий путь к файлу\n{path_to_excel}\nХотите изменить???", reply_markup=kb_yes_cancel()
        )
        await state.set_state(ChangePathsToExcel.change_path_to_excel)
    except Exception:
        await message.answer(
            text="Файл хранения данных отсутствует.\n"
                 "Введите команду /create"
        )


@router.message(ChangePathsToExcel.change_path_to_excel, F.text.lower() == "да")
async def change_path_to_excel(message: Message, state: FSMContext):
    await message.answer(
        text="Введите путь к файлу"
             "\nв формате папка1/папка2/файл.xlsx",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(ChangePathsToExcel.input_path_to_excel)


@router.message(ChangePathsToExcel.input_path_to_excel, F.text)
async def input_path_to_excel(message: Message, state: FSMContext):
    path_to_excel = message.text
    with open("data/path_to_excel.txt", "w", encoding="utf-8") as file:
        file.write(path_to_excel)
    await state.clear()
    await message.answer(text=f"Готово!!!\nТекущий путь к файлу\n{path_to_excel}")


@router.message(Command(commands=["help"]), AdminFilter(is_admin=True))
async def cmd_help(message: Message):
    await message.answer(text="Help!!!")


@router.message(Command(commands=["create"]), AdminFilter(is_admin=True))
async def cmd_work(message: Message):
    if not os.path.exists("data"):
        os.mkdir("data")

    if not os.path.exists("data/path_to_save.txt"):
        path_to_save = "tmp/"
        with open("data/path_to_save.txt", "w", encoding="utf-8") as file:
            file.write(path_to_save)

    if not os.path.exists("data/path_to_excel.txt"):
        path_to_excel = "!technical_specification/codes_120723.xlsx"
        with open("data/path_to_excel.txt", "w", encoding="utf-8") as file:
            file.write(path_to_excel)

    await message.answer(text="Все необходимые файлы для работы - СОЗДАНЫ!")
