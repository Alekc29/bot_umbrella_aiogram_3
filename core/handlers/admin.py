from aiogram import Bot, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from config import DEV_ID
from core.keyboards.replykey import admin
from core.utils.class_fsm import FSMPost
from core.utils.data_base import DataBase


router = Router()


@router.message(Command('moderator'))
async def get_admin_keyboards(message: Message):
    if message.from_user.id == DEV_ID:
        await message.answer('Что босс надо?',
                             reply_markup=admin)
        await message.delete()
    else:
        await message.answer('Вы не являетесь администратором бота.')
        await message.delete()


@router.message(Command('Рассылка'))
async def mailing_post_bot(message: Message, state: FSMContext):
    if message.from_user.id == DEV_ID:
        await message.answer('Набери пост для рассылки по юзерам.')
        await message.delete()
        await state.set_state(FSMPost.post)


async def send_message_to_users(users, message: Message, bot: Bot):
    ''' функция для рассылки сообщения по списку пользователей '''
    for user in users:
        try:
            await bot.send_message(user[0],
                                   f'{message.text}')
        except Exception:
            await bot.send_message(
                DEV_ID,
                f'Произошла ошибка при отправке сообщения юзеру: {user[0]}'
            )


@router.message(FSMPost.post)
async def send_mailing_bot(message: Message,
                           bot: Bot,
                           state: FSMContext):
    if message.from_user.id == DEV_ID:
        db = DataBase('users.db')
        users = db.get_users()
        await send_message_to_users(users, message, bot)
        await message.answer(
            f"Рассылка сообщения завершена. Отправлено сообщений: {len(users)}"
        )
        await state.clear()


@router.message(Command('Статистика'))
async def get_statistics(message: Message):
    if message.from_user.id == DEV_ID:
        db = DataBase('users.db')
        await message.answer(f'Кол-во юзеров: {db.count_all_users()}')
        await message.delete()


@router.message(Command('Клиент'))
async def change_client_command(message: Message):
    if message.from_user.id == DEV_ID:
        await message.answer('Вы перешли в клиентскую часть.',
                             reply_markup=ReplyKeyboardRemove())
        await message.delete()
