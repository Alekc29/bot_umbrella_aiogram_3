from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

geo = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Отправить гео', request_location=True),
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
