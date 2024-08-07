import aiohttp

from core.utils.data_base import DataBase
from config import API_KEY_WEATHER

NUM_DAYS = 16


async def check_weather(chat_id: int):
    ''' Выдаёт текущую погоду по названию города или координатам. '''
    db = DataBase('users.db')
    city = db.get_city(chat_id)
    async with aiohttp.ClientSession() as session:
        if city:
            async with session.get(
                f'https://api.openweathermap.org/data/2.5/weather?'
                f'q={city}&appid={API_KEY_WEATHER}&units=metric'
            ) as response:
                data = await response.json()
                description = data['weather'][0]['main']
                tempreture = round(data['main']['temp'])
                wind = round(data['wind']['speed'])
                return [description, tempreture, wind, city]
        lat, lon = db.get_geo(chat_id)
        async with session.get(
            f'https://api.openweathermap.org/data/2.5/weather?'
            f'lat={lat}&lon={lon}&lang=ru&appid={API_KEY_WEATHER}&units=metric'
        ) as response:
            data = await response.json()
            description = data['weather'][0]['main']
            tempreture = round(data['main']['temp'])
            wind = round(data['wind']['speed'])
            city = data['name']
            db.add_city(chat_id, city)
            return [description, tempreture, wind, city]


async def check_weather_5_day(chat_id: int):
    ''' Выдаёт погоду за 5 дней по названию города или координатам. '''
    db = DataBase('users.db')
    city = db.get_city(chat_id)
    async with aiohttp.ClientSession() as session:
        if city:
            async with session.get(
                f'https://api.openweathermap.org/data/2.5/forecast?'
                f'q={city}&appid={API_KEY_WEATHER}&units=metric'
            ) as response:
                data = await response.json()
                description = []
                tempreture = []
                wind = []
                dt_txt = []
                for inc in range(0, NUM_DAYS):
                    description.append(data['list'][inc]['weather'][0]['main'])
                    tempreture.append(data['list'][inc]['main']['temp'])
                    wind.append(data['list'][inc]['wind']['speed'])
                    dt_txt.append(data['list'][inc]['dt_txt'])
                return [description, tempreture, wind, dt_txt, city]
        lat, lon = db.get_geo(chat_id)
        async with session.get(
            f'https://api.openweathermap.org/data/2.5/forecast?'
            f'lat={lat}&lon={lon}&lang=ru&appid={API_KEY_WEATHER}&units=metric'
        ) as response:
            data = await response.json()
            description = []
            tempreture = []
            wind = []
            dt_txt = []
            for inc in range(0, NUM_DAYS):
                description.append(data['list'][inc]['weather'][0]['main'])
                tempreture.append(data['list'][inc]['main']['temp'])
                wind.append(data['list'][inc]['wind']['speed'])
                dt_txt.append(data['list'][inc]['dt_txt'])
            city = data['city']['name']
            db.add_city(chat_id, city)
            return [description, tempreture, wind, dt_txt, city]
