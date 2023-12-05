from aiogram.types import Message
from aiogram.filters import BaseFilter
from admins import ADMIN


class AdminFilter(BaseFilter):
    def __init__(self, is_admin):
        self.is_admin = is_admin

    async def __call__(self, message: Message):
        user = message.from_user.id
        return user in ADMIN
