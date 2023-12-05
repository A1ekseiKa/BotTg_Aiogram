from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def kb_client_cancel() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Отмена")
    kb.adjust(1)

    return kb.as_markup(resize_keyboard=True)


def kb_client() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Подтвердить")
    kb.button(text="Отмена")
    kb.adjust(2)

    return kb.as_markup(resize_keyboard=True)


def kb_client_delivery() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Загрузить")
    kb.adjust(1)

    return kb.as_markup(resize_keyboard=True)
