import os
import requests

from dotenv import load_dotenv
from aiogram import Dispatcher, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from core.utils.data_base import DataBase
from core.utils.class_fsm import FSMTown


load_dotenv()
API_KEY_WEATHER = os.getenv('API_KEY_WEATHER')
DEV_ID = os.getenv('DEV_ID')


# @dp.message_handler(commands=['start', 'help'])
# async def command_start(message: Message):
#     try:
#         if not db.user_exists(message.from_user.id):
#             db.add_user(message.from_user.id, message.from_user.first_name)
#         await bot.send_message(
#             message.from_user.id,
#             'Привет! Я буду напоминать тебе брать зонтик в дождливую погоду.',
#             reply_markup=kb_client
#         )
#         await message.delete()
#     except Exception as ex:
#         print(ex)
#         await message.reply(
#             'Общение с ботом через ЛС, напишите ему:\nhttps://t.me/reminder_umbrella_bot'
#         )


async def get_town(message: Message, state: FSMContext):
    ''' Задать город для получения напоминания взять зонтик. '''
    await message.answer('Напишите свой город.')
    await message.delete()
    await state.set_state(FSMTown.town)
    

async def cancel_handler(message: Message,
                         state: FSMContext):
    ''' Выход из машины состояний. '''
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.clear()
    await message.reply('Ok')


async def load_town_base(message: Message,
                         state: FSMContext):
    ''' Ловим ответ по городу для напоминания про зонтик. '''
    try:
        db = DataBase('users.db')
        db.add_city(message.from_user.id, message.text)
        await message.answer(f'Ваш город {message.text} успешно занесён в базу.')
        await state.update_data(town=message.text)
        await state.set_state(FSMTown.reminder_time)
    except Exception as ex:
        print(ex)
        await message.answer(message.from_user.id,
                             'Произошла ошибка при занесении в базу.')


async def get_time(message: Message):
    ''' Задать время для получения напоминания взять зонтик. '''
    await FSMTime.timer.set()
    await message.answer('В какое время вы встаёте? Ответ напишите в формате чч:мм.')
    await message.delete()


async def load_timer_base(message: Message,
                          state: FSMContext):
    ''' Ловим ответ по времени для напоминания про зонтик. '''
    await message.answer(f'Ваше время {message.text} успешно занесёно в базу.')
    context_data = await state.get_data()

    await state.clear()
    # try:
    #     async with state.proxy() as data:
    #         data['timer'] = message.text
    #     db.add_timer(message.from_user.id, message.text)
    #     await state.finish()
    #     await bot.send_message(message.from_user.id,
    #                            'Ваше время успешно занесёно в базу.')
    # except Exception as ex:
    #     print(ex)
    #     await bot.send_message(message.from_user.id,
    #                            'Произошла ошибка при занесении в базу.')


async def get_wish(message: Message):
    ''' Просит оставить пожелание разработчику. '''
    await FSMWish.wish.set()
    await message.answer('Оставьте пожелание разработчику, если передумали напишите: отмена.')
    await message.delete()


async def load_wish_base(message: Message,
                              state: FSMContext):
    ''' Ловим ответ по пожеланию для разработчика. '''
    try:
        async with state.proxy() as data:
            data['wish'] = message.text
        await bot.send_message(DEV_ID,
                               f'Пожелание от {message.from_user.first_name}: {message.text}')
        await state.finish()
        await bot.send_message(message.from_user.id,
                               'Ваше пожелание отправлено разработчику.')
    except Exception as ex:
        print(ex)
        await bot.send_message(message.from_user.id,
                               'Произошла ошибка при отправке пожелания.')

# @dp.message_handler(commands=['Погода'])
async def get_weather(message: Message):
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
            await bot.send_message(message.from_user.id,
                                f'погода в {city}\n'+
                                f'Температура: {tempreture}C\n'+
                                f'Скорость ветра: {winds} m/c\n{description}')
            await message.delete()
        except Exception as ex:
            print(ex)
            await bot.send_message(message.from_user.id,
                                f'Проверьте название города.')
    
