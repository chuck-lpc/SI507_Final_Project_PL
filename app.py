from flask import Flask, render_template, request
import sqlite3
from db_init import *
from web_api_data_retrieve import *

app = Flask(__name__)


def get_currency_value(currency):
    conn = sqlite3.connect('SteamAppPrice.db')
    cur = conn.cursor()

    q = f'''
        SELECT price
        FROM CURRENCY
        WHERE currency = '{currency}'
    '''

    ret = cur.execute(q).fetchone()[0]
    conn.close()
    return ret



def convert_currency(value, base, target):
    base_value = get_currency_value(base)
    target_value = get_currency_value(target)

    ret = value / base_value * target_value
    return ret




@app.route('/')
def index():
    return render_template('index.html')

@app.route('/results', methods=['POST'])
def results():
    steamid = request.form['steamid']
    target_currency = request.form['currency']
    order = request.form['order']
    region = request.form['region']
    symbols = "USD,JPY,GBP,CNY,EUR,INR,AUD,CAD,MXN,PLN"
    currency_data = get_currencies_for_query(symbols)
    if currency_data:
        save_currencies_to_db(currency_data)
    else:
        print('No currency data retrived')
    games = get_games_for_user(steamid, region)
    if games:
        save_games_to_db(games)
        if order == 'appid':
            games = sorted(games, key=lambda x: x.appid)
        elif order == 'name':
            games = sorted(games, key=lambda x: x.name)
        elif order == 'price':
            games = sorted(games, key=lambda x: x.price)
        else:
            raise ValueError("Unknown order option")
        origin_value = str(round(sum([each.price for each in games]), 2))
        origin_currency = games[0].currency
        converted_value = str(round(convert_currency(float(origin_value), origin_currency, target_currency), 2))

        return render_template('results.html', 
            games=games, 
            origin_value=origin_value, origin_currency=origin_currency,
            converted_value=converted_value , currency_to_convert=target_currency, 
            steamid=steamid)
    else:
        return "Nothing retrived"


if __name__ == '__main__':
    #CACHE_DICT = open_cache()
    #steamid = '76561198439501171'
    #games = get_games_for_user(steamid)
    initialize_db()
    app.run(debug=True)