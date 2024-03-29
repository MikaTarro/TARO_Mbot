import sqlite3


class Database:
    def __init__(self, db_name):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self.create_db()

    def create_db(self):
        try:
            query = ("""CREATE TABLE IF NOT EXISTS users(
                         id INTEGER PRIMARY KEY,
                         user_name TEXT,
                         user_phone TEXT,
                         telegram_id TEXT);
                         CREATE TABLE IF NOT EXISTS place(
                         id INTEGER PRIMARY KEY,
                         name_place TEXT,
                         place_address TEXT);
                         CREATE TABLE IF NOT EXISTS events(
                         id INTEGER PRIMARY KEY,
                         place_id TEXT,
                         date_event TEXT,
                         time_event TEXT)""")
            self.cursor.executescript(query)
            self.connection.commit()
        except sqlite3.Error as Error:
            print("Ошибка при создании:", Error)

    def add_user(self, user_name, user_phone, telegram_id):
        self.cursor.execute(f"INSERT INTO users (user_name, user_phone, telegram_id) VALUES (?,?,?)",
                            (user_name, user_phone, telegram_id))
        self.connection.commit()

    def add_event(self, place_id, date_event, time_event):
        self.cursor.execute(f"INSERT INTO events (place_id, date_event, time_event) VALUES (?,?,?)",
                            (place_id, date_event, time_event))
        self.connection.commit()

    def select_user_id(self, telegram_id):
        users = self.cursor.execute("SELECT * FROM users WHERE telegram_id = ?", (telegram_id,))
        return users.fetchone()

    def db_select_column(self, table_name, column, item):
        result = self.cursor.execute("SELECT * FROM {} WHERE {} = {}".format(table_name, column, item))
        return result

    def db_select_all(self, table_name):
        result = self.cursor.execute("SELECT * FROM {}".format(table_name))
        return result.fetchall()

    def select_events(self, status, data_event):
        result = self.cursor.execute(
            "SELECT * FROM 'events' JOIN 'place' ON place_id = place.id WHERE 'status' = '{}' AND 'date_event' = '{}'"
            .format(status, data_event))
        return result.fetchall()

    def select_person(self, event_id): # соединяем 2 таблицы по полю телеграм Айди
        result = self.cursor.execute(
            "SELECT * FROM 'record_events' JOIN 'users' ON 'record_events'.'user_telegram_id' = 'users'.'telegram_id' WHERE 'record_events'.'event_id' = {}"
            .format(event_id))
        return result.fetchall()

    def check_user(self, event_id, user_id):
        result = self.cursor.execute(
            "SELECT * FROM 'record_events' WHERE 'event_id' = {} AND 'user_telegram_id' = {}".format(event_id, user_id))
        return result.fetchall()

    def __del__(self):
        self.cursor.close()
        self.connection.close()
