import sqlite3
import os.path
from os import path


def initialize_db():
    if path.exists('SteamAppPrice.db'):
        print('Data base exists. Using existing database')
    else:
        print('Initializing data base....')
        conn = sqlite3.connect('SteamAppPrice.db')
        c = conn.cursor()
        #c.execute('''CREATE TABLE APPS
        #         ([id] INTEGER PRIMARY KEY, [appid] INTEGER, [NAME] text, [price] float, [currency] text)''')
        c.execute('''CREATE TABLE APPS
                ([appid] INTEGER, 
                [NAME] text, 
                [price] float, 
                [currency] text, 
                UNIQUE(appid, NAME, price, currency))''')
        c.execute('''CREATE TABLE CURRENCY
                ([currency] text PRIMARY KEY, 
                [price] float, 
                UNIQUE(currency, price))''')
        conn.commit()
        conn.close()
    return