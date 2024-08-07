from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault


async def set_commands_main(bot: Bot):
    commands = [
        BotCommand(
            command='weather',
            description='Узнать погоду сейчас'
        ),
        BotCommand(
            command='carwash',
            description='Стоит ли мыть машину???'
        ),
        BotCommand(
            command='profile',
            description='Ваш профиль'
        ),
        BotCommand(
            command='help',
            description='Помощь'
        ),
        BotCommand(
            command='off',
            description='Отключить напоминание'
        ),
    ]
    await bot.set_my_commands(commands, BotCommandScopeDefault())
