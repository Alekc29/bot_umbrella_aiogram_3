from aiogram import Bot
from aiogram.types import Message

from core.utils.data_base import DataBase

async def get_start(message: Message, bot: Bot):
    db = DataBase('users.db')
    if not db.user_exists(message.from_user.id):
        db.add_user(message.from_user.id, message.from_user.first_name)
    await bot.send_message(
        message.from_user.id,
        f'Привет! Я буду напоминать тебе брать зонтик в дождливую погоду.'
    )


async def get_photo(message: Message, bot: Bot):
    await message.answer(f'Ты отправил картинку!')
    file = await bot.get_file(message.photo[-1].file_id)
    await bot.download_file(file.file_path, 'photo.jpg')


async def get_hello(message: Message, bot: Bot):
    await message.answer(f'И тебе привет!')