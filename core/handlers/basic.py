from aiogram import Bot, F, Router
from aiogram.filters import Command
from aiogram.types import Message

from core.utils.data_base import DataBase
from core.utils.db_connect import PgData
router = Router()


@router.message(Command(commands=['start', 'run', 'help']))
async def get_start(message: Message, bot: Bot):
    #await db.add_user(message.from_user.id, message.from_user.first_name)
    db = DataBase('users.db')
    if not db.user_exists(message.from_user.id):
        db.add_user(message.from_user.id, message.from_user.first_name)
    await message.answer(
        'Привет! Я буду напоминать тебе брать зонтик в дождливую погоду. '
        'Для начала работы укажите город через /city '
        'и время напоминания через /time. '
        'Для получения информации о текущей погоде напишите /weather'
    )


@router.message(F.photo)
async def get_photo(message: Message, bot: Bot):
    await message.answer('Ты отправил картинку!')
    file = await bot.get_file(message.photo[-1].file_id)
    await bot.download_file(file.file_path, 'photo.jpg')


@router.message(F.text == 'Привет')
async def get_hello(message: Message):
    await message.answer('И тебе привет!')


@router.message()
async def get_echo(message: Message):
    await message.answer(
        'Такой команды я не знаю! В меню есть все доступные команды.'
    )
