import re
from datetime import datetime

from aiogram import Bot, F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from config import BASE, DEV_ID

from core.keyboards.replykey import client_profile, geo
from core.utils.class_fsm import FSMTown, FSMWash, FSMWish
from core.utils.data_base import DataBase
from core.utils.weather import check_weather, check_weather_5_day

router = Router()


@router.message(F.text.in_(['Город', '/city']))
async def get_town(message: Message, state: FSMContext):
    ''' Задать город для получения напоминания взять зонтик. '''
    await message.answer('Напишите свой город или отправьте геолокацию.',
                         reply_markup=geo)
    await message.delete()
    await state.set_state(FSMTown.town)


@router.message(F.text.in_(['отмена', 'Отмена', 'cancel', '/cancel']))
async def cancel_handler(message: Message,
                         state: FSMContext,
                         bot: Bot):
    ''' Выход из машины состояний. '''
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.clear()
    await message.answer('Ok', reply_markup=ReplyKeyboardRemove())
    await message.delete()


@router.message(FSMTown.town)
async def load_town_base(message: Message,
                         state: FSMContext):
    ''' Ловим ответ по городу для напоминания про зонтик. '''
    if message.location:
        db = DataBase(BASE)
        db.add_geo(message.from_user.id,
                   round(message.location.latitude, 2),
                   round(message.location.longitude, 2))
        await message.answer(
            'Ваша геолокация успешно занесена в базу.\n'
            'Теперь введите время напоминания в формате <u>чч:мм</u>.',
            reply_markup=ReplyKeyboardRemove()
        )
        db.add_city(message.from_user.id, message.text)
        await state.update_data(town=message.text)
        await state.set_state(FSMTown.reminder_time)
    else:
        try:
            text = message.text.lower()
            pattern = r'[A-Za-zа-яё]+( [A-Za-zа-яё]+)*'
            city_good = re.fullmatch(pattern, text)
            if city_good:
                db = DataBase('umb_users.db')
                db.add_city(message.from_user.id, message.text.title())
                await message.answer(
                    f'Ваш город <b><u>{message.text.title()}</u></b> '
                    'успешно занесён в базу.\n'
                    'Теперь введите время напоминания в формате <u>чч:мм</u>.',
                    reply_markup=ReplyKeyboardRemove()
                )
                await state.set_state(FSMTown.reminder_time)
            else:
                await message.answer(
                    'Произошла ошибка! Убедитесь,'
                    'что название города верно написано.\n'
                    'Повторите попытку ввода или отправьте геолокацию.'
                )
        except Exception as ex:
            print(ex)
            await message.answer('Произошла ошибка при занесении в базу.',
                                 reply_markup=ReplyKeyboardRemove())


@router.message(F.text.in_(['Время', '/time']))
async def get_time(message: Message,
                   state: FSMContext):
    ''' Задать время для получения напоминания взять зонтик. '''
    await message.answer(
        'В какое время вы встаёте? Ответ напишите в формате <u>чч:мм</u>.'
    )
    await message.delete()
    await state.set_state(FSMTown.reminder_time)


@router.message(FSMTown.reminder_time)
async def load_timer_base(message: Message,
                          state: FSMContext,
                          apscheduler: AsyncIOScheduler,
                          bot: Bot):
    ''' Ловим ответ по времени для напоминания про зонтик. '''
    try:
        time = message.text
        pattern = r'\d{2}\W\d{2}'
        time_good = re.fullmatch(pattern, time)
        if time_good:
            time = time.replace(time[2], ':')
            hours, minutes = time.split(':')
            db = DataBase(BASE)
            db.add_timer(message.from_user.id, time)
            await message.answer(
                f'Ваше время <u>{time}</u> успешно занесёно в базу.',
                reply_markup=ReplyKeyboardRemove()
            )
            await state.clear()
        else:
            await message.answer(
                'Время напоминания введено некорректно! Повторите попытку.'
            )
    except Exception as ex:
        print(ex)
        await message.answer('Произошла ошибка при занесении в базу.')
    try:
        apscheduler.add_job(send_reminder_umbrella,
                            trigger='cron',
                            id=str(message.from_user.id),
                            hour=int(hours),
                            minute=int(minutes),
                            start_date=datetime.now(),
                            kwargs={'bot': bot,
                                    'chat_id': message.from_user.id})
    except Exception as ex:
        print(ex)
        await message.answer('Произошла ошибка при подключении таймера.')


@router.message(F.text == 'Пожелание')
async def get_wish(message: Message,
                   state: FSMContext):
    ''' Просит оставить пожелание разработчику. '''
    await message.answer('Оставьте пожелание разработчику,'
                         'если передумали выберите в меню: отмена.')
    await message.delete()
    await state.set_state(FSMWish.wish)


@router.message(FSMWish.wish)
async def load_wish_base(message: Message,
                         bot: Bot,
                         state: FSMContext):
    ''' Ловим ответ по пожеланию для разработчика. '''
    await bot.send_message(
        DEV_ID,
        f'Пожелание от {message.from_user.first_name}: {message.text}'
    )
    await state.clear()
    await message.answer('Ваше пожелание отправлено разработчику.')
    await message.delete()


@router.message(F.text == 'Автомойка')
async def get_wash(message: Message,
                   state: FSMContext):
    ''' Просит ввести количество дней для мойки авто. '''
    await message.answer('Укажите количество дней, которое я буду проверять, '
                         'чтобы выдать рекомендацию по мойке машины. '
                         'Количество дней может быть от 1 до 5. '
                         'Прогноза погода на более 5 дней я не знаю. '
                         'Если передумали выберите в меню: отмена.')
    await message.delete()
    await state.set_state(FSMWash.wash)


@router.message(FSMWash.wash)
async def load_wash_base(message: Message,
                         bot: Bot,
                         state: FSMContext):
    ''' Ловим ответ по количеству дней для проверки автомойки. '''
    try:
        num_days = int(message.text)
        if 0 < num_days < 6:
            db = DataBase(BASE)
            db.add_num_days(message.from_user.id, num_days)
            days = {1: 'день',
                    2: 'дня',
                    3: 'дня',
                    4: 'дня',
                    5: 'дней'}
            await message.answer(
                'Теперь, когда ты спросишь меня, стоит ли мыть машину, '
                f'я буду проверять погоду за {num_days} {days[num_days]}.',
                reply_markup=ReplyKeyboardRemove()
            )
            await state.clear()
        else:
            await message.answer(
                'Количество дней введено некорректно! Повторите попытку.'
                'Число должно быть больше либо равно 1, '
                'но меньше либо равно 5.'
            )
    except Exception as ex:
        print(ex)
        await message.answer('Произошла ошибка при занесении в базу.')
    await message.delete()


async def send_reminder_umbrella(bot: Bot, chat_id: int):
    ''' Проверяет идёт ли дождь и отправляет сообщение напоминание. '''
    try:
        description, tempreture, wind, city = await check_weather(chat_id)
        if description == 'rain':
            await bot.send_message(chat_id,
                                   'Возьми зонтик! Сегодня будет дождик!')
        else:
            await bot.send_message(chat_id,
                                   'Сегодня зонтик не пригодится!\n' +
                                   f'На улице {tempreture} градусов.')
    except Exception as ex:
        print(ex)
        await bot.send_message(chat_id,
                               'Проверьте название города.')


@router.message(Command('weather'))
async def get_weather(message: Message):
    ''' Показывает текущюю погоду. '''
    try:
        description, tempreture, wind, city = await check_weather(
            message.from_user.id
        )
        await message.answer(f'погода в городе: {city}\n'
                             f'Температура: {tempreture} C\n'
                             f'Скорость ветра: {wind} m/c\n{description}')
        await message.delete()
    except Exception as ex:
        print(ex)
        await message.answer('Проверьте название города.')


@router.message(Command('carwash'))
async def get_carwash(message: Message):
    ''' Выдаёт рекомендацию стоит ли мыть машину по прогнозу на 3 дня. '''
    try:
        description, temp, wind, dt_txt, city = await check_weather_5_day(
            message.from_user.id
        )
        if 'Rain' in description:
            await message.answer('Не советую мыть машину, будет дождь.')
        else:
            await message.answer('Машину стоит помыть! '
                                 'В ближайшие дни дождя не будет!')
        await message.delete()
    except Exception as ex:
        print(ex)
        await message.answer('Проверьте название города.')


@router.message(Command('profile'))
async def get_profile(message: Message, bot: Bot):
    ''' Выдаёт информацию из базы пользователю. '''
    db = DataBase(BASE)
    try:
        city = db.get_city(message.from_user.id)
        time = db.get_timer(message.from_user.id)
        num_days = db.get_num_days(message.from_user.id)
        await message.answer(f'{message.from_user.first_name}\n'
                             f'город: {city}\n'
                             f'время напоминания: {time}\n'
                             f'дней перед мойкой авто: {num_days}',
                             reply_markup=client_profile)
        await message.delete()
    except Exception as ex:
        print(ex)
        await message.answer('Произошла ошибка при обращении к базе.')


@router.message(Command('off'))
async def off_reminder(message: Message,
                       bot: Bot,
                       apscheduler: AsyncIOScheduler,):
    ''' Выключает напоминание. '''
    db = DataBase(BASE)
    try:
        db.add_timer(message.from_user.id, None)
        await message.answer('Напоминание успешно отключено.')
        await message.delete()
    except Exception as ex:
        print(ex)
        await message.answer('Произошла ошибка при обращении к базе.')
    try:
        apscheduler.remove_job(job_id=str(message.from_user.id))
    except Exception as ex:
        print(ex)
        await message.answer(
            'Произошла ошибка при удалении таймера напоминания.'
        )
