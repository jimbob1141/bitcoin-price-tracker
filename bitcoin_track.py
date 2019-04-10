import requests
import json
import time
from sqlalchemy import create_engine

engine = create_engine('postgresql://james:iz5npo@localhost:5432/postgres')
engine.connect()
def process_request():
    old_data = {}
    while True:
        try:
            btc_data = requests.get("https://api.coinmarketcap.com/v1/ticker/")
            json_data = json.loads(btc_data.text)
        except requests.exceptions.ConnectionError:
            print('Connection refused, retying...')
            continue
        for coin_dict in json_data:
            if coin_dict['id'] not in old_data.keys():
                old_data[coin_dict['id']] = coin_dict['last_updated']
            if coin_dict['last_updated'] != old_data[coin_dict['id']]:
                print(coin_dict['last_updated'], ": ", old_data[coin_dict['id']])
                coin_id = coin_dict['id']
                symbol = coin_dict['symbol']
                rank = coin_dict['rank']
                price_usd = coin_dict['price_usd']
                price_btc = coin_dict['price_btc']
                volume_usd_24h = coin_dict['24h_volume_usd']
                market_cap_usd = coin_dict['market_cap_usd']
                available_supply = coin_dict['available_supply']
                total_supply = coin_dict['total_supply']
                max_supply = coin_dict['max_supply']
                if max_supply == None:
                    max_supply = 'NULL'
                percent_change_1h = coin_dict['percent_change_1h']
                percent_change_24h = coin_dict['percent_change_24h']
                percent_change_7d = coin_dict['percent_change_7d']
                last_updated = coin_dict['last_updated']
                statement = ('INSERT INTO crypto_currency (coin_id,' +
                                                            'symbol,' +
                                                            'rank,' +
                                                            'price_usd,' +
                                                            'price_btc,' +
                                                            'volume_usd_24h,' +
                                                            'market_cap_usd,' +
                                                            'available_supply,' +
                                                            'total_supply,' +
                                                            'max_supply,' +
                                                            'percent_change_1h,' +
                                                            'percent_change_24h,' +
                                                            'percent_change_7d,' +
                                                            'last_updated)' +
                                                            "VALUES ('" +
                                                            coin_id + "','" +
                                                            symbol + "'," +
                                                            str(rank) + ',' +
                                                            str(price_usd) + ',' +
                                                            str(price_btc) + ',' +
                                                            str(volume_usd_24h) + ',' +
                                                            str(market_cap_usd) + ',' +
                                                            str(available_supply) + ',' +
                                                            str(total_supply) + ',' +
                                                            str(max_supply) + ',' +
                                                            str(percent_change_1h) + ',' +
                                                            str(percent_change_24h) + ',' +
                                                            str(percent_change_7d) + ',' +
                                                            str(last_updated) + ');')
                engine.execute(statement)
                old_data[coin_dict['id']] = coin_dict['last_updated']
        time.sleep(30)     

process_request()                                        
