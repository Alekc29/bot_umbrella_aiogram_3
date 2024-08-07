import asyncio
import contextlib
import logging

from asyncpg import create_pool
from aiogram import Bot, Dispatcher
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from config import BOT_TOKEN, DEV_ID
from core.handlers import admin, basic, client
from core.middlewares.apschedulermiddleware import SchedulerMiddleware
from core.utils.commands import set_commands_main
from core.middlewares.dbmiddleware import db_session


async def start_bot(bot: Bot):
    await set_commands_main(bot)
    await bot.send_message(DEV_ID, text='Бот запущен!')


async def stop_bot(bot: Bot):
    await bot.send_message(DEV_ID, text='Бот остановлен!')


async def create_pool_db():
    return await create_pool(user='postgres',
                             password='postgres',
                             database='users',
                             host='127.0.0.1',
                             port=5432,
                             command_timeout=60)


async def start():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - [%(levelname)s] - %(name)s - "
               "(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"
    )
    bot = Bot(token=BOT_TOKEN, parse_mode='HTML')
    #pool_connect_db = await create_pool_db()
    dp = Dispatcher()
    #dp.update.middleware.register(db_session(pool_connect_db))
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
