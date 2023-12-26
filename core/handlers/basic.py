from aiogram import Bot, Router, F
from aiogram.types import Message
from aiogram.filters import Command

from core.utils.data_base import DataBase

router = Router()


@router.message(Command(commands=['start', 'run']))
async def get_start(message: Message, bot: Bot):
    db = DataBase('users.db')
    if not db.user_exists(message.from_user.id):
        db.add_user(message.from_user.id, message.from_user.first_name)
    await bot.send_message(
        message.from_user.id,
        f'Привет! Я буду напоминать тебе брать зонтик в дождливую погоду.'
    )


@router.message(F.photo)
async def get_photo(message: Message, bot: Bot):
    await message.answer(f'Ты отправил картинку!')
    file = await bot.get_file(message.photo[-1].file_id)
    await bot.download_file(file.file_path, 'photo.jpg')


@router.message(F.text == 'Привет')
async def get_hello(message: Message, bot: Bot):
    await message.answer(f'И тебе привет!')