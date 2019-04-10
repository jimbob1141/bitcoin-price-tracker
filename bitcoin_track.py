import requests
import json
import time
from sqlalchemy import create_engine

#creates db engine, password needs setting
engine = create_engine('postgresql://james:iz5npo@localhost:5432/postgres')
engine.connect()
def process_request():
    #initialises a dictionary to store previous data
    old_data = {}
    while True:
        #attempts http request and catches exceptions to auto retry failed attempts
        try:
            btc_data = requests.get("https://api.coinmarketcap.com/v1/ticker/")
            json_data = json.loads(btc_data.text)
        except requests.exceptions.ConnectionError:
            print('Connection refused, retying...')
            continue
        #loops through each coin's data and populates the old data dictionary
        #adds the ID's and their last updated times for later comparison
        for coin_dict in json_data:
            if coin_dict['id'] not in old_data.keys():
                old_data[coin_dict['id']] = coin_dict['last_updated']
            #compares current last updated with old_data last updated
            #this is based on the id for the coin, this stops the database being populated with duplicate values
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
                #max supply can be None, this isn't suitable for the database query, so I set it to the Null string instead
                if max_supply == None:
                    max_supply = 'NULL'
                percent_change_1h = coin_dict['percent_change_1h']
                percent_change_24h = coin_dict['percent_change_24h']
                percent_change_7d = coin_dict['percent_change_7d']
                last_updated = coin_dict['last_updated']
                #builds the query based on the variables
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
                #executes the statement, inserting the values into the database
                engine.execute(statement)
                #updates the old data dictionary for the particular coin with the new last updated value
                old_data[coin_dict['id']] = coin_dict['last_updated']
        #the data doesn't update that often, so waiting for 30 seconds is fine, prevents the ip becoming blacklisted because of excess requests
        time.sleep(30)     
#runs the main function
process_request()                                        
