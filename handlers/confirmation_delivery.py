import os

import pendulum
from aiogram import Router, Bot, F
from aiogram.filters import Command
from aiogram.fsm.state import default_state
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message

from keyboards import client_kb
from main import load_xlsx, get_address

router = Router()

List_photo = {}


class DeliveryPublication(StatesGroup):
    search_id = State()
    upload_foto = State()


@router.message(Command(commands=["delivery"]))
@router.message(default_state, F.text.lower() == "загрузить")
async def cmd_delivery(message: Message, state: FSMContext):
    await state.set_state(DeliveryPublication.search_id)
    await message.answer(text="Введите ID адреса ", reply_markup=client_kb.kb_client_cancel())


@router.message(DeliveryPublication.search_id)
async def process_name(message: Message, state: FSMContext):
    await state.update_data(address_id=message.text)
    data = await state.get_data()

    with open("data/path_to_excel.txt", encoding="utf-8") as file:
        path_to_excel = file.read()

    address_list = load_xlsx(path_to_excel)
    building_address = get_address(address_list, data['address_id'])
    if building_address is not None:
        await state.update_data(
            publication_code=building_address[0],
            publication_name=building_address[1],
            building_street=building_address[2],
            building_number=building_address[3],
            building_body=building_address[4],
            address_id=building_address[5]
        )
        await state.set_state(DeliveryPublication.upload_foto)
        await message.answer(text="Загружайте фото", reply_markup=client_kb.kb_client())
    else:
        await message.answer(text="Что-то пошло не так.\nПроверьте адрес ID!",
                             reply_markup=client_kb.kb_client_cancel())


@router.message(DeliveryPublication.upload_foto)
async def upload_foto(message: Message, bot: Bot, state: FSMContext) -> None:
    global List_photo
    data = await state.get_data()

    key = str(message.from_user.id)
    List_photo.setdefault(key, [])

    if message.content_type == 'photo':
        List_photo[key].append(message.photo[-1].file_id)

    elif message.content_type == 'text' and len(List_photo[key]) == 0:
        await message.answer(
            text="Вы забыли добавить фотографии..."
        )
    elif message.content_type == 'text':
        try:
            with open("data/path_to_save.txt", encoding="utf-8") as file:
                path_to_save = file.read()

            if not os.path.exists(f'{path_to_save}'):
                os.mkdir(f'{path_to_save}')

            if not os.path.exists(f'{path_to_save}{data["publication_name"]}/'):
                os.mkdir(f'{path_to_save}{data["publication_name"]}')

            if not os.path.exists(
                    f'{path_to_save}{data["publication_name"]}/{pendulum.now().start_of("week").format("DD_MM_YYYY")}/'):
                os.mkdir(
                    f'{path_to_save}{data["publication_name"]}/{pendulum.now().start_of("week").format("DD_MM_YYYY")}/')

            for keys, values in List_photo.items():
                for number, value in enumerate(values):
                    await bot.download(
                        value,
                        destination=f'{path_to_save}{data["publication_name"]}/{pendulum.now().start_of("week").format("DD_MM_YYYY")}'
                                    f'/{pendulum.now().format("DD_MM_YYYY_HH-mm-ss_")}{data["building_street"]}'
                                    f'_д.{data["building_number"]}_к.{data["building_body"]}_{number + 1}.jpg'
                    )
            await message.answer(text=f"Загружено фото: {len(List_photo[key])}")
            await bot.send_message(message.from_user.id, 'Готово', reply_markup=client_kb.kb_client_delivery())
            List_photo[key].clear()
            await state.clear()
        except Exception:
            await message.answer(
                text="Что-то пошло не так. Обратитесь к администратору"
            )
