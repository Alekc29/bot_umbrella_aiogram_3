from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

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
            KeyboardButton(text='Пожелание'),
            KeyboardButton(text='отмена'),
        ]
    ],
    resize_keyboard=True
)