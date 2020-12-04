import sqlite3

conn = sqlite3.connect('SteamAppPrice.db')
c = conn.cursor()
c.execute('''CREATE TABLE APPS
         ([id] INTEGER PRIMARY KEY, [appid] INTEGER, [NAME] text, [price] float, [currency] text)''')
c.execute('''CREATE TABLE CURRENCY
         ([currency] text, [price] float)''')
conn.commit()
