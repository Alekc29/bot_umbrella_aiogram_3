import asyncio
import contextlib
import logging
import os

from aiogram import Bot, Dispatcher
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dotenv import load_dotenv

from core.handlers import admin, basic, client
from core.utils.apschedulermiddleware import SchedulerMiddleware
from core.utils.commands import set_commands_main

load_dotenv()

API_KEY_WEATHER = os.getenv('API_KEY_WEATHER')
BOT_TOKEN = os.getenv('BOT_TOKEN')
DEV_ID = os.getenv('DEV_ID')


async def start_bot(bot: Bot):
    await set_commands_main(bot)
    await bot.send_message(DEV_ID, text='Бот запущен!')


async def stop_bot(bot: Bot):
    await bot.send_message(DEV_ID, text='Бот остановлен!')


async def start():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - [%(levelname)s] - %(name)s - "
               "(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"
    )
    bot = Bot(token=BOT_TOKEN, parse_mode='HTML')
    dp = Dispatcher()
    scheduler = AsyncIOScheduler(timezone='Europe/Moscow')
    scheduler.start()
    dp.update.middleware.register(SchedulerMiddleware(scheduler))
    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)
    dp.include_routers(
        client.router,
        admin.router,
        basic.router,
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
