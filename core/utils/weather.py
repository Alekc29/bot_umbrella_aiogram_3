import aiohttp

from main import API_KEY_WEATHER
from core.utils.data_base import DataBase


async def check_weather(chat_id: int):
    db = DataBase('users.db')
    city = db.get_city(chat_id)
    async with aiohttp.ClientSession() as session:
        if city:
            async with session.get(
                f'https://api.openweathermap.org/data/2.5/weather?' +
                f'q={city}&appid={API_KEY_WEATHER}&units=metric'
            ) as response:
                data = await response.json()
                description = data['weather'][0]['main']
                tempreture = round(data['main']['temp'])
                wind = round(data['wind']['speed'])
                return [description, tempreture, wind, city]
        lat, lon = db.get_geo(chat_id)
        async with session.get(
            f'https://api.openweathermap.org/data/2.5/weather?' +
            f'lat={lat}&lon={lon}&lang=ru&appid={API_KEY_WEATHER}&units=metric'
        ) as response:
            data = await response.json()
            description = data['weather'][0]['main']
            tempreture = round(data['main']['temp'])
            wind = round(data['wind']['speed'])
            city = data['name']
            db.add_city(chat_id, city)
            return [description, tempreture, wind, city]
