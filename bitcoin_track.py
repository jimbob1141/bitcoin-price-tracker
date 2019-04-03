import requests
import json
from matplotlib import pyplot
import time
btc_time = []
btc_price = []


def get_data():
    new_data = ''
    old_data = ''
    while True
    btc = requests.get("https://api.coinmarketcap.com/v1/ticker/bitcoin/")
    new_data = json.loads(btc.text)
    if new_data != old_data:
        btc_time.append(new_data[0]['last_updated'])
        btc_price.append(new_data[0]['price_usd'])
    old_data = new_data
    if len(btc_time) % 10 == 0:
        graph_make(btc_time, btc_price)


def graph_make(btc_time, btc_price):
    pyplot.scatter(btc_time, btc_price)
    pyplot.show()


while True:
    get_data()
    time.sleep(1)
