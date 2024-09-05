from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                           KeyboardButton, ReplyKeyboardMarkup)

geo = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Отправить гео', request_location=True),
            KeyboardButton(text='отмена'),
        ]
    ],
    resize_keyboard=True
)

admin = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='/Рассылка'),
            KeyboardButton(text='/Статистика'),
            KeyboardButton(text='/Клиент'),
        ]
    ],
    resize_keyboard=True
)

client_profile = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Город'),
            KeyboardButton(text='Время'),
            KeyboardButton(text='Автомойка'),
        ],
        [
            KeyboardButton(text='Пожелание'),
            KeyboardButton(text='отмена'),
        ]
    ],
    resize_keyboard=True
)

client_weather = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Погода сейчас',
                                 callback_data='weather_1_day'),
        ],
        [
            InlineKeyboardButton(text='Погода на 3 дня',
                                 callback_data='weather_3_days'),
        ],
        [
            InlineKeyboardButton(text='Погода на 5 дней',
                                 callback_data='weather_5_days'),
        ]
    ]
)
