from requests_oauthlib import OAuth1
import json
import requests
import sqlite3
from bs4 import BeautifulSoup

CACHE_FILENAME = "steam_owned_apps_cache.json"
CACHE_DICT = {}

def open_cache():
    ''' Opens the cache file if it exists and loads the JSON into
    the CACHE_DICT dictionary.
    if the cache file doesn't exist, creates a new cache dictionary
    
    Parameters
    ----------
    None
    
    Returns
    -------
    The opened cache: dict
    '''
    try:
        cache_file = open(CACHE_FILENAME, 'r')
        cache_contents = cache_file.read()
        cache_dict = json.loads(cache_contents)
        cache_file.close()
    except:
        cache_dict = {}
    return cache_dict

def save_cache(cache_dict):
    ''' Saves the current state of the cache to disk
    
    Parameters
    ----------
    cache_dict: dict
        The dictionary to save
    
    Returns
    -------
    None
    '''
    dumped_json_cache = json.dumps(cache_dict)
    fw = open(CACHE_FILENAME,"w")
    fw.write(dumped_json_cache)
    fw.close() 

def construct_unique_key(baseurl, params):
    ''' constructs a key that is guaranteed to uniquely and 
    repeatably identify an API request by its baseurl and params

    AUTOGRADER NOTES: To correctly test this using the autograder, use an underscore ("_") 
    to join your baseurl with the params and all the key-value pairs from params
    E.g., baseurl_key1_value1
    
    Parameters
    ----------
    baseurl: string
        The URL for the API endpoint
    params: dict
        A dictionary of param:value pairs
    
    Returns
    -------
    string
        the unique key as a string
    '''
    #TODO Implement function
    param_strings = []
    connector = '_'
    for k in sorted(params.keys()):
        param_strings.append(f'{k}_{params[k]}')
    unique_key = baseurl + connector + connector.join(param_strings)
    return unique_key

def make_request(baseurl, params):
    '''Make a request to the Web API using the baseurl and params
    
    Parameters
    ----------
    baseurl: string
        The URL for the API endpoint
    params: dictionary
        A dictionary of param:value pairs
    
    Returns
    -------
    dict
        the data returned from making the request in the form of 
        a dictionary
    '''
    #TODO Implement function
    ret = requests.get(baseurl, params=params).json()
    return ret

def make_request_with_cache_steam(baseurl, key, steamid, format_data):
    '''Check the cache for a saved result for this baseurl+params:values
    combo. If the result is found, return it. Otherwise send a new 
    request, save it, then return it.

    AUTOGRADER NOTES: To test your use of caching in the autograder, please do the following:
    If the result is in your cache, print "fetching cached data"
    If you request a new result using make_request(), print "making new request"

    Do no include the print statements in your return statement. Just print them as appropriate.
    This, of course, does not ensure that you correctly retrieved that data from your cache, 
    but it will help us to see if you are appropriately attempting to use the cache.
    
    Parameters
    ----------
    baseurl: string
        The URL for the API endpoint
    hashtag: string
        The hashtag to search for
    count: integer
        The number of results you request from Twitter
    
    Returns
    -------
    dict
        the results of the query as a dictionary loaded from cache
        JSON
    '''
    #TODO Implement function
    CACHE_DICT = open_cache()
    params = {'steamid': steamid, 'format': format_data}
    params_with_key = {'key': key, 'steamid': steamid, 'format': format_data}
    unique_key = construct_unique_key(baseurl, params)
    if unique_key in CACHE_DICT:
        print("fetching cached data")
        return CACHE_DICT[unique_key]
    else:
        print("making new request")
        ret = make_request(baseurl, params_with_key)
        CACHE_DICT[unique_key] = ret
        save_cache(CACHE_DICT)
        return ret


def make_request_with_cache_currency(baseurl, access_key, symbols, data_format):
    '''Check the cache for a saved result for this baseurl+params:values
    combo. If the result is found, return it. Otherwise send a new 
    request, save it, then return it.

    AUTOGRADER NOTES: To test your use of caching in the autograder, please do the following:
    If the result is in your cache, print "fetching cached data"
    If you request a new result using make_request(), print "making new request"

    Do no include the print statements in your return statement. Just print them as appropriate.
    This, of course, does not ensure that you correctly retrieved that data from your cache, 
    but it will help us to see if you are appropriately attempting to use the cache.
    
    Parameters
    ----------
    baseurl: string
        The URL for the API endpoint
    hashtag: string
        The hashtag to search for
    count: integer
        The number of results you request from Twitter
    
    Returns
    -------
    dict
        the results of the query as a dictionary loaded from cache
        JSON
    '''
    #TODO Implement function
    CACHE_DICT = open_cache()
    params = {'symbols': symbols, 'format': data_format}
    params_with_key = {'access_key': access_key, 'symbols': symbols, 'format': data_format}
    unique_key = construct_unique_key(baseurl, params)
    if unique_key in CACHE_DICT:
        print("fetching cached data")
        return CACHE_DICT[unique_key]
    else:
        print("making new request")
        ret = make_request(baseurl, params_with_key)
        CACHE_DICT[unique_key] = ret
        save_cache(CACHE_DICT)
        return ret

class Game:
    def __init__(self, appid, name, price, currency):
        self.appid = appid
        self.name = name
        self.price = price
        self.currency = currency


def get_soup_with_cache(url):
    ''' Get the soup with the help of cache
    
    Parameters
    ----------
    url: string
        The url to fetch
    
    Returns
    -------
    soup: BeautifulSoup
        The returned soup
    '''
    CACHE_DICT = open_cache()
    if url in CACHE_DICT:
        print("Using cache")
        response = CACHE_DICT[url]
        soup = BeautifulSoup(response, 'html.parser')
    else:
        print("Fetching")
        response = requests.get(url)
        CACHE_DICT[url] = response.text
        save_cache(CACHE_DICT)
        soup = BeautifulSoup(response.text, 'html.parser')
    
    return soup


def get_game_instance(appid):
    print(appid)
    game_url = 'https://store.steampowered.com/app/'+str(appid)
    soup = get_soup_with_cache(game_url)
    
    name = soup.find('div', class_ = 'apphub_AppName').text.strip()

    #print(soup.find('div', class_ = 'game_purchase_price price'))
    try:
        price = float(soup.find('div', class_ = 'game_purchase_price price')['data-price-final'])/100
    except:
        if(soup.find('div', class_ = 'game_purchase_price price').text.strip() == 'Free to Play'):
            price = 0
        else:
            raise ValueError('Unknown price')
    currency = soup.find('meta', itemprop = "priceCurrency")['content']



    ret = Game(appid, name, price, currency)

    return ret


def get_games_for_user(steamid):
    steam_data = make_request_with_cache_steam(steam_baseurl, steam_key, steamid, steam_format_data)
    ret = []
    for each in steam_data['response']['games']:
        appid = each['appid']
        try:
            game_instance = get_game_instance(appid)
        except:
            print("Unknown appid: {}".format(appid))
            continue
        ret.append(game_instance)

    return ret




if __name__ == "__main__":
    conn = sqlite3.connect('SteamAppPrice.db')
    c = conn.cursor()

    CACHE_DICT = open_cache()
    steam_baseurl = "http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/"
    steam_key = '7F374A23BA3BD0391B8860562E98B9B9'
    steamid = '76561198439501171'
    steam_format_data = 'json'

    #steam_data = make_request_with_cache_steam(steam_baseurl, steam_key, steamid, steam_format_data)
    games = get_games_for_user(steamid)

    for i in range(len(games)):
        c.execute('''INSERT INTO APPS VALUES (?,?,?,?,?)''', [i, games[i].appid, games[i].name, games[i].price, games[i].currency])


    currency_baseurl = "http://data.fixer.io/api/latest"
    currency_key = "9509f2d09e274f6442c08b2359883dde"
    symbols = "USD,AUD,CAD,PLN,MXN"
    currency_format = '1'

    currency_data = make_request_with_cache_currency(currency_baseurl, currency_key, symbols, currency_format)

    for key in currency_data['rates']:
        c.execute('''INSERT INTO CURRENCY VALUES (?,?)''', [key, currency_data['rates'][key]])

    conn.commit()


    

