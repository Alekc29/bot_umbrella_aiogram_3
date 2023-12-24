import sqlite3


class DataBase:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cur = self.connection.cursor()

    def user_exists(self, user_id):
        ''' Проверяет есть ли юзер в базе. '''
        with self.connection:
            result = self.cur.execute('''
                SELECT * 
                FROM users 
                WHERE user_id = ?;
            ''', (user_id,)).fetchall()
            return bool(len(result))
        
    def add_user(self, user_id, user_name, city=None, timer=None):
        ''' Создаёт нового пользователя. '''
        with self.connection:
            return self.cur.execute('''
                INSERT INTO users ('user_id', 'user_name')
                VALUES (?, ?);
            ''', (user_id, user_name,))
        
    def add_city(self, user_id, town):
        ''' Изменяет город для прогноза. '''
        with self.connection:
            return self.cur.execute('''
                UPDATE users 
                SET city = ?
                WHERE user_id = ?;
            ''', (town, user_id,))
        
    def add_timer(self, user_id, timer):
        ''' Изменяет время напоминания. '''
        with self.connection:
            return self.cur.execute('''
                UPDATE users 
                SET timer = ?
                WHERE user_id = ?;
            ''', (timer, user_id,))

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
        
    def get_timer(self, user_id):
        ''' Выдаёт время из базы по id. '''
        with self.connection:
            return self.cur.execute('''
                SELECT timer
                FROM users
                WHERE user_id = ?;
            ''', (user_id,)).fetchone()[0]
        
    def count_all_users(self):
        with self.connection:
            return self.cur.execute('''
                SELECT COUNT('user_id') as count 
                FROM users;
            ''').fetchone()[0]


def sql_start():
    global base, cur
    base = sqlite3.connect('users.db')
    cur = base.cursor()
    if not base:
        return 'Произошла ошибка при подключении базы.'
    base.execute('CREATE TABLE IF NOT EXISTS users(user_id TEXT PRIMARY KEY, user_name TEXT, city TEXT, timer TEXT)')
    base.commit()
