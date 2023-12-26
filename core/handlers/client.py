import os
import requests

from dotenv import load_dotenv
from aiogram import Bot, Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from core.utils.data_base import DataBase
from core.utils.class_fsm import FSMTown, FSMWish

load_dotenv()
API_KEY_WEATHER = os.getenv('API_KEY_WEATHER')
DEV_ID = os.getenv('DEV_ID')

router = Router()


@router.message(Command('city'))
async def get_town(message: Message, state: FSMContext):
    ''' Задать город для получения напоминания взять зонтик. '''
    await message.answer('Напишите свой город.')
    await message.delete()
    await state.set_state(FSMTown.town)
    

@router.message(Command('cancel'))
async def cancel_handler(message: Message,
                         state: FSMContext):
    ''' Выход из машины состояний. '''
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.clear()
    await message.answer('Ok')
    await message.delete()


@router.message(FSMTown.town)
async def load_town_base(message: Message,
                         state: FSMContext):
    ''' Ловим ответ по городу для напоминания про зонтик. '''
    try:
        db = DataBase('users.db')
        db.add_city(message.from_user.id, message.text)
        await message.answer(f'Ваш город {message.text} успешно занесён в базу.'
                             f'Теперь введите время напоминания в формате чч:мм.')
        await state.update_data(town=message.text)
        await state.set_state(FSMTown.reminder_time)
    except Exception as ex:
        print(ex)
        await message.answer(message.from_user.id,
                             'Произошла ошибка при занесении в базу.')


@router.message(Command('time'))
async def get_time(message: Message,
                   state: FSMContext):
    ''' Задать время для получения напоминания взять зонтик. '''
    await message.answer('В какое время вы встаёте? Ответ напишите в формате чч:мм.')
    await message.delete()
    await state.set_state(FSMTown.reminder_time)


@router.message(FSMTown.reminder_time)
async def load_timer_base(message: Message,
                          state: FSMContext):
    ''' Ловим ответ по времени для напоминания про зонтик. '''
    try:
        db = DataBase('users.db')
        db.add_timer(message.from_user.id, message.text)
        await message.answer(f'Ваше время {message.text} успешно занесёно в базу.')
        await state.clear()
    except Exception as ex:
        print(ex)
        await message.answer(f'Произошла ошибка при занесении в базу.')


@router.message(Command('wish'))
async def get_wish(message: Message,
                   state: FSMContext):
    ''' Просит оставить пожелание разработчику. '''
    await message.answer('Оставьте пожелание разработчику, если передумали напишите: отмена.')
    await message.delete()
    await state.set_state(FSMWish.wish)


@router.message(FSMWish.wish)
async def load_wish_base(message: Message,
                         bot: Bot,
                         state: FSMContext):
    ''' Ловим ответ по пожеланию для разработчика. '''
    await bot.send_message(DEV_ID,
                           f'Пожелание от {message.from_user.first_name}: {message.text}')
    await state.clear()
    await message.answer(f'Ваше пожелание отправлено разработчику.')
    

@router.message(Command('weather'))
async def get_weather(message: Message):
    db = DataBase('users.db')
    city = db.get_city(message.from_user.id)
    if city:
        try:
            req = requests.get(
                f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY_WEATHER}&units=metric'
            )
            data = req.json()
            description = data['weather'][0]['main']
            tempreture = data['main']['temp']
            winds = data['wind']['speed']
            await message.answer(f'погода в {city}\n'+
                                 f'Температура: {tempreture}C\n'+
                                 f'Скорость ветра: {winds} m/c\n{description}')
            await message.delete()
        except Exception as ex:
            print(ex)
            await message.answer(f'Проверьте название города.')
    
