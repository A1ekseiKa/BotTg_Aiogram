import asyncio
import logging
import sys
from dotenv import load_dotenv
import os

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode


from handlers import admin, common, confirmation_delivery

dp = Dispatcher()


async def main():
    load_dotenv()
    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    bot = Bot(os.getenv('MY_TOKEN'), parse_mode=ParseMode.HTML)

    dp.include_routers(admin.router)
    dp.include_routers(common.router)
    dp.include_routers(confirmation_delivery.router)

    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    try:
        logging.basicConfig(level=logging.INFO, stream=sys.stdout)
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Bot stopped!")
