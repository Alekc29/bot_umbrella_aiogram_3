import aiohttp
from config import API_KEY_WEATHER

from core.utils.data_base import DataBase


async def check_weather(chat_id: int):
    ''' Выдаёт текущую погоду по названию города или координатам. '''
    db = DataBase('umb_users.db')
    city = db.get_city(chat_id)
    async with aiohttp.ClientSession() as session:
        if city:
            async with session.get(
                f'https://api.openweathermap.org/data/2.5/weather?'
                f'q={city}&appid={API_KEY_WEATHER}&units=metric'
            ) as response:
                data = await response.json()
        else:
            lat, lon = db.get_geo(chat_id)
            async with session.get(
                f'https://api.openweathermap.org/data/2.5/weather?'
                f'lat={lat}&lon={lon}&lang=ru&'
                f'appid={API_KEY_WEATHER}&units=metric'
            ) as response:
                data = await response.json()
                city = data['name']
                db.add_city(chat_id, city)
        description = data['weather'][0]['main']
        tempreture = round(data['main']['temp'])
        temp_max = round(data['main']['temp_max'])
        wind = round(data['wind']['speed'])
        return [description, tempreture, temp_max, wind, city]


async def check_weather_5_day(chat_id: int):
    ''' Выдаёт погоду за 5 дней по названию города или координатам. '''
    db = DataBase('umb_users.db')
    city = db.get_city(chat_id)
    num_days = db.get_num_days(chat_id)
    num_days *= 8
    async with aiohttp.ClientSession() as session:
        if city:
            async with session.get(
                f'https://api.openweathermap.org/data/2.5/forecast?'
                f'q={city}&appid={API_KEY_WEATHER}&units=metric'
            ) as response:
                data = await response.json()
        else:
            lat, lon = db.get_geo(chat_id)
            async with session.get(
                f'https://api.openweathermap.org/data/2.5/forecast?'
                f'lat={lat}&lon={lon}&lang=ru&'
                f'appid={API_KEY_WEATHER}&units=metric'
            ) as response:
                data = await response.json()
                city = data['city']['name']
                db.add_city(chat_id, city)
        description = []
        tempreture = []
        wind = []
        dt_txt = []
        for inc in range(0, num_days):
            description.append(data['list'][inc]['weather'][0]['main'])
            tempreture.append(data['list'][inc]['main']['temp'])
            wind.append(data['list'][inc]['wind']['speed'])
            dt_txt.append(data['list'][inc]['dt_txt'])
        return [description, tempreture, wind, dt_txt, city]
