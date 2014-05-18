__author__ = 'MrTrustworthy'

from datetime import datetime
import sqlite3
from app_config import DB_URI
import error_handling

def setup_tables():

    with sqlite3.connect(DB_URI) as connection:
        cursor = connection.cursor()
        cursor.execute("""CREATE TABLE users(
                        name text PRIMARY KEY,
                        password text
                        )""")
        cursor.execute("""CREATE TABLE chatlogs(
                        id integer PRIMARY KEY AUTOINCREMENT,
                        day text,
                        time text,
                        name text,
                        post text
                        )""")

print
# USER MANAGEMENT
def add_user(name, password):
    with sqlite3.connect(DB_URI) as connection:
        cursor = connection.cursor()
        cursor.execute("""INSERT INTO users VALUES (?, ?)""", (name, password))
        if cursor.rowcount == 0:
            raise error_handling.DatabaseQueryFailed("add user")


def confirm_user_login(name, password):
    with sqlite3.connect(DB_URI) as connection:
        cursor = connection.cursor()
        cursor.execute("""SELECT password FROM users WHERE name=?""", (name,))
        password_tuple = cursor.fetchone()
        if password_tuple is None:
            raise error_handling.UserDoesNotExist(name)
        elif password_tuple[0] != password:
            raise error_handling.WrongPassword(name)
        elif password_tuple[0] == password:
            return True
        return False


def all_users():
    with sqlite3.connect(DB_URI) as connection:
        cursor = connection.cursor()
        cursor.execute("""SELECT * FROM users""")
        result = cursor.fetchall()
        return result


# CHATLOG MANAGEMENT
def add_chatlog(name, text):
    with sqlite3.connect(DB_URI) as connection:
        cursor = connection.cursor()
        date_now = str(datetime.now())[:10]
        time_now = str(datetime.now())[11:19]
        cursor.execute("""INSERT INTO chatlogs VALUES (NULL, ?, ?, ?, ?)""", (date_now, time_now, name, text))
        if cursor.rowcount == 0:
            raise error_handling.DatabaseQueryFailed("add chatlog")


def get_chatlogs(number_of_items=20):
    with sqlite3.connect(DB_URI) as connection:
        cursor = connection.cursor()
        cursor.execute("""SELECT * FROM chatlogs""")
        result = cursor.fetchall()
        return result

def delete_chatlog(id):
    with sqlite3.connect(DB_URI) as connection:
        cursor = connection.cursor()
        cursor.execute("""DELETE FROM chatlogs WHERE id=?""", (id,))
        if cursor.rowcount == 0:
            raise error_handling.DatabaseQueryFailed("delete chatlog")


def demo():
    setup_tables()

    add_user("jim", "1234")
    add_user("ad", "min")

    add_chatlog("ad", "this is a test entry")

if __name__ == "__main__":
    setup_tables()
    #demo()
