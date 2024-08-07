from aiogram import BaseMiddleware
from typing import Any, Awaitable, Callable, Dict

from aiogram.types import TelegramObject
from asyncpg.pool import Pool

from core.utils.db_connect import PgData


class db_session(BaseMiddleware):
    def __init__(self, connector: Pool):
        super().__init__()
        self.connector = connector

    async def __call__(self,
                       handler: Callable[
                           [TelegramObject,
                            Dict[str, Any]],
                           Awaitable[Any]
                       ],
                       event: TelegramObject,
                       data: Dict[str, Any]) -> Any:
        async with self.connector.acquire() as connect:
            data['request'] = PgData(connect)
            return await handler(event, data)
