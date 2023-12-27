import requests

from main import API_KEY_WEATHER
from core.utils.data_base import DataBase


async def check_weather(chat_id: int):
    try:
        db = DataBase('users.db')
        city = db.get_city(chat_id)
    except Exception as ex:
        print(ex)
    if city:
        req = requests.get(
            f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY_WEATHER}&units=metric'
        )
        data = req.json()
        description = data['weather'][0]['main']
        tempreture = data['main']['temp']
        wind = data['wind']['speed']
        return [description, tempreture, wind, city]
    else:
        return [0,0,0,0]