from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault


async def set_commands(bot: Bot):
    commands = [
        BotCommand(
            command='profile',
            description='Ваш профиль'
        ),
        BotCommand(
            command='help',
            description='Помощь'
        ),
        BotCommand(
            command='city',
            description='Задать город'
        ),
        BotCommand(
            command='time',
            description='Задать время напоминания'
        ),
        BotCommand(
            command='cancel',
            description='Сбросить'
        ),
    ]
    await bot.set_my_commands(commands, BotCommandScopeDefault())