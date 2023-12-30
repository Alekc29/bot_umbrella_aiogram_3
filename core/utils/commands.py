from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault


async def set_commands(bot: Bot):
    commands = [
        BotCommand(
            command='city',
            description='Задать город'
        ),
        BotCommand(
            command='time',
            description='Задать время напоминания'
        ),
        BotCommand(
            command='weather',
            description='Узнать погоду сейчас'
        ),
        BotCommand(
            command='profile',
            description='Ваш профиль'
        ),
        BotCommand(
            command='wish',
            description='Пожелание разработчику'
        ),
        BotCommand(
            command='help',
            description='Помощь'
        ),
        BotCommand(
            command='cancel',
            description='Отмена'
        ),
    ]
    await bot.set_my_commands(commands, BotCommandScopeDefault())