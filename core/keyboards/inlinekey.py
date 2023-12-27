from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

geo = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Отправить гео', request_location=True),
        ]
    ],
    resize_keyboard=True
)