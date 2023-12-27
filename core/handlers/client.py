import requests

from datetime import datetime
from aiogram import Bot, Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from main import API_KEY_WEATHER, DEV_ID
from core.utils.data_base import DataBase
from core.utils.class_fsm import FSMTown, FSMWish
from core.utils.weather import check_weather
from core.keyboards.inlinekey import geo

router = Router()


@router.message(Command('city'))
async def get_town(message: Message, state: FSMContext):
    ''' Задать город для получения напоминания взять зонтик. '''
    await message.answer('Напишите свой город.', reply_markup=geo)
    await message.delete()
    await state.set_state(FSMTown.town)


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
                          state: FSMContext,
                          apscheduler: AsyncIOScheduler,
                          bot: Bot):
    ''' Ловим ответ по времени для напоминания про зонтик. '''
    try:
        db = DataBase('users.db')
        db.add_timer(message.from_user.id, message.text)
        await message.answer(f'Ваше время {message.text} успешно занесёно в базу.')
        await state.clear()
        hours, minutes = message.text.split(':')
        apscheduler.add_job(send_reminder_umbrella,
                            trigger='cron',
                            hour=int(hours),
                            minute=int(minutes),
                            start_date=datetime.now(),
                            kwargs={'bot': bot,
                                    'chat_id': message.from_user.id})
    except Exception as ex:
        print(ex)
        await message.answer(f'Произошла ошибка при занесении в базу.')


@router.message(Command('wish'))
async def get_wish(message: Message,
                   state: FSMContext):
    ''' Просит оставить пожелание разработчику. '''
    await message.answer('Оставьте пожелание разработчику, если передумали выберите в меню: отмена.')
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
    

async def send_reminder_umbrella(bot: Bot, chat_id: int):
    
    db = DataBase('users.db')
    city = db.get_city(chat_id)
    if city:
        try:
            req = requests.get(
                f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY_WEATHER}&units=metric'
            )
            data = req.json()
            description = data['weather'][0]['main']
            tempreture = data['main']['temp']
            if description == 'rain':
                await bot.send_message(chat_id,
                                       f'Возьми зонтик! Сегодня будет дождик!')
            else:
                await bot.send_message(chat_id,
                                       f'Сегодня зонтик не пригодится! На улице {round(tempreture)} градусов.')
        except Exception as ex:
            print(ex)
            await bot.send_message(chat_id,
                                   f'Проверьте название города.')


@router.message(Command('weather'))
async def get_weather(message: Message):
    try:
        description, tempreture, wind, city = check_weather(message.from_user.id)
        await message.answer(f'погода в {city}\n'+
                             f'Температура: {tempreture}C\n'+
                             f'Скорость ветра: {wind} m/c\n{description}')
        await message.delete()
    except Exception as ex:
        print(ex)
        await message.answer(f'Проверьте название города.')
    

@router.message(Command('profile'))
async def get_profile(message: Message):
    db = DataBase('users.db')
    try:
        city = db.get_city(message.from_user.id)
        time = db.get_timer(message.from_user.id)
        await message.answer(f'{message.from_user.first_name}\n'+
                             f'город: {city}\n'+
                             f'время напоминания: {time}')
        await message.delete()
    except Exception as ex:
        print(ex)
        await message.answer(f'Произошла ошибка при обращении к базе.')
