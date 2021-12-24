import sqlite3 as sql
from sqlite3 import Error
import telegram
import telegram.ext

db = "world.db"

def create_or_connect():
    con = None
    try:
        con = sql.connect(db)
    except Error as e:
        print(e)
    finally:
        return con

def main():
    