import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from dotenv import load_dotenv

from core.handlers import basic, client
from core.utils.commands import set_commands
from core.utils.class_fsm import FSMTown
from core.utils.data_base import sql_start, DataBase


load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
DEV_ID = os.getenv('DEV_ID')

data = sql_start()
db = DataBase('users.db')

async def start_bot(bot: Bot):
    await set_commands(bot)
    await bot.send_message(DEV_ID, text='Бот запущен!')
    
    if data:
        await bot.send_message(DEV_ID, text=data)


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
    dp.message.register(client.get_town,
                        Command(commands='Задать_город'))
    dp.message.register(client.load_town_base, FSMTown.town)
    dp.message.register(client.load_timer_base, FSMTown.reminder_time)
    dp.message.register(basic.get_photo,
                        F.photo)
    dp.message.register(basic.get_hello,
                        F.text == 'Привет')
    dp.message.register(basic.get_start,
                        Command(commands=['start', 'run']))
    try:
        await dp.start_polling(bot)
    except Exception as ex: 
        logging.error(f'Exception - {ex}', exc_info=True)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(start())