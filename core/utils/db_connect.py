from asyncpg.pool import Pool


class PgData:
    def __init__(self, connector: Pool):
        self.connector = connector
        self.create_db()

    async def create_db(self):
        ''' Создаёт базу Postgresql с именем users. '''
        try:
            await self.connector.execute(
                'CREATE TABLE IF NOT EXISTS users('
                'user_id INTEGER PRIMARY KEY,'
                'user_name TEXT,'
                'city TEXT,'
                'lat FLOAT,'
                'lon FLOAT,'
                'reminder_time TEXT);'
            )
        except Exception as ex:
            print(f'Ошибка при создании базы Postgres. {ex}')

    async def add_user(self,
                       user_id,
                       user_name,
                       city=None,
                       lat=None,
                       lon=None,
                       reminder_time=None):
        ''' Создаёт нового пользователя. '''
        await self.connector.execute(
            '''
                INSERT INTO users ('user_id', 'user_name')
                VALUES (?, ?);
            ''', (user_id, user_name,))
