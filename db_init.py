import sqlite3

conn = sqlite3.connect('SteamAppPrice.db')
c = conn.cursor()
#c.execute('''CREATE TABLE APPS
#         ([id] INTEGER PRIMARY KEY, [appid] INTEGER, [NAME] text, [price] float, [currency] text)''')
c.execute('''CREATE TABLE APPS
         ([appid] INTEGER PRIMARY KEY, 
         [NAME] text, 
         [price] float, 
         [currency] text, 
         UNIQUE(appid, NAME, price, currency))''')
c.execute('''CREATE TABLE CURRENCY
         ([currency] text PRIMARY KEY, 
         [price] float, 
         UNIQUE(currency, price))''')
conn.commit()
