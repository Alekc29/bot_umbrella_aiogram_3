import sqlite3


class DataBase:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cur = self.connection.cursor()
        self.create_db()

    def create_db(self):
        try:
            query = ('CREATE TABLE IF NOT EXISTS users('
                     'user_id INTEGER PRIMARY KEY,'
                     'user_name TEXT,'
                     'city TEXT,'
                     'lat FLOAT,'
                     'lon FLOAT,'
                     'reminder_time TEXT,'
                     'num_days INTEGER);')
            self.cur.execute(query)
            self.connection.commit()
        except sqlite3.Error as ex:
            print(f'Ошибка при создании базы: {ex}.')

    def __dell__(self):
        self.cur.close()
        self.connection.close()

    def user_exists(self, user_id):
        ''' Проверяет есть ли юзер в базе. '''
        with self.connection:
            result = self.cur.execute('''
                SELECT *
                FROM users
                WHERE user_id = ?;
            ''', (user_id,)).fetchall()
            return bool(len(result))

    def add_user(self,
                 user_id,
                 user_name,
                 city=None,
                 lat=None,
                 lon=None,
                 reminder_time=None,
                 num_days=2):
        ''' Создаёт нового пользователя. '''
        with self.connection:
            return self.cur.execute('''
                INSERT INTO users ('user_id', 'user_name', 'num_days')
                VALUES (?, ?, ?);
            ''', (user_id, user_name, num_days))

    def add_city(self, user_id, town):
        ''' Изменяет город для прогноза. '''
        with self.connection:
            return self.cur.execute('''
                UPDATE users
                SET city = ?
                WHERE user_id = ?;
            ''', (town, user_id,))

    def add_geo(self, user_id, lat, lon):
        ''' Изменяет геолокацию для прогноза. '''
        with self.connection:
            return self.cur.execute('''
                UPDATE users
                SET lat = ?, lon = ?
                WHERE user_id = ?;
            ''', (lat, lon, user_id,))

    def add_timer(self, user_id, reminder_time):
        ''' Изменяет время напоминания. '''
        with self.connection:
            return self.cur.execute('''
                UPDATE users
                SET reminder_time = ?
                WHERE user_id = ?;
            ''', (reminder_time, user_id,))

    def add_num_days(self, user_id, num_days):
        ''' Изменяет количество дней мойки авто. '''
        with self.connection:
            return self.cur.execute('''
                UPDATE users
                SET num_days = ?
                WHERE user_id = ?;
            ''', (num_days, user_id,))

    def get_users(self):
        with self.connection:
            return self.cur.execute('''
                SELECT user_id
                FROM users;
            ''').fetchall()

    def get_city(self, user_id):
        ''' Выдаёт город из базы по id. '''
        with self.connection:
            return self.cur.execute('''
                SELECT city
                FROM users
                WHERE user_id = ?;
            ''', (user_id,)).fetchone()[0]

    def get_geo(self, user_id):
        ''' Выдаёт геолокацию из базы по id. '''
        with self.connection:
            return self.cur.execute('''
                SELECT lat, lon
                FROM users
                WHERE user_id = ?;
            ''', (user_id,)).fetchone()

    def get_timer(self, user_id):
        ''' Выдаёт время из базы по id. '''
        with self.connection:
            return self.cur.execute('''
                SELECT reminder_time
                FROM users
                WHERE user_id = ?;
            ''', (user_id,)).fetchone()[0]

    def get_num_days(self, user_id):
        ''' Выдаёт дни для мойки авто из базы по id. '''
        with self.connection:
            return self.cur.execute('''
                SELECT num_days
                FROM users
                WHERE user_id = ?;
            ''', (user_id,)).fetchone()[0]

    def count_all_users(self):
        with self.connection:
            return self.cur.execute('''
                SELECT COUNT('user_id') as count
                FROM users;
            ''').fetchone()[0]
