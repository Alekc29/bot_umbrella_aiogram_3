import os

from dotenv import load_dotenv
from aiogram import Bot, Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from core.utils.data_base import DataBase
from core.utils.class_fsm import FSMPost
from core.keyboards.replykey import admin

load_dotenv()

DEV_ID = int(os.getenv('DEV_ID'))

router = Router()


@router.message(Command('moderator'))
async def get_admin_keyboards(message: Message):
    if message.from_user.id == DEV_ID:
        await message.answer('Что босс надо?',
                             reply_markup=admin)
        await message.delete()
    else:
        await message.answer(f'Вы не являетесь администратором бота.')
        await message.delete()


@router.message(Command('Рассылка'))
async def mailing_post_bot(message: Message, state: FSMContext):
    if message.from_user.id == DEV_ID:
        await message.answer('Набери пост для рассылки по юзерам.')
        await message.delete()
        await state.set_state(FSMPost.post)


# Выход из состояний
# async def cancel_handler(message: types.Message,
#                          state: FSMContext):
#     if message.from_user.id == ID:
#         current_state = await state.get_state()
#         if current_state is None:
#             return
#         await state.finish()
#         await message.reply('Ok')


async def send_message_to_users(users, message: Message, bot: Bot):
    ''' функция для рассылки сообщения по списку пользователей '''
    for user in users:
        try:
            await bot.send_message(user[0],
                                   f'{message.text}')
        except Exception as e:
            await bot.send_message(DEV_ID,
                                   f'Произошла ошибка при отправке сообщения юзеру: {user}')


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
        await message.answer(f'Вы перешли в клиентскую часть.',
                             reply_markup=ReplyKeyboardRemove())
        await message.delete()
