import asyncio
import logging
import os
import contextlib

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

from core.handlers import basic, client
from core.utils.commands import set_commands

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
DEV_ID = os.getenv('DEV_ID')


async def start_bot(bot: Bot):
    await set_commands(bot)
    await bot.send_message(DEV_ID, text='Бот запущен!')


async def stop_bot(bot: Bot):
    await bot.send_message(DEV_ID, text='Бот остановлен!')


async def start():
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s - [%(levelname)s] - %(name)s - "
                               "(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s")
    bot = Bot(token=BOT_TOKEN, parse_mode='HTML')
    dp = Dispatcher()
    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)
    dp.include_routers(
        basic.router,
        client.router
    )
    try:
        await dp.start_polling(bot)
    except Exception as ex: 
        logging.error(f'Exception - {ex}', exc_info=True)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    with contextlib.suppress(KeyboardInterrupt, SystemExit):
        asyncio.run(start())