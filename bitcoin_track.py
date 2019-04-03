import requests
import json
import time
from matplotlib import pyplot

#declaring lists that will be appended too.
#will later be swapped out with a sql db, this is only temporary
btc_time = []
btc_price = []


def get_data():
    #used for comparison as the data refreshes irregularly
    new_data = ''
    old_data = ''
    #Loops continuously
    while True
      #gets current btc information
      btc = requests.get("https://api.coinmarketcap.com/v1/ticker/bitcoin/")
      #converts the string response to json
      new_data = json.loads(btc.text)
        #compares new data to the previous data returned, if the data has changed it appends
        #the new data to the lists
        if new_data != old_data:
          btc_time.append(new_data[0]['last_updated'])
          btc_price.append(new_data[0]['price_usd'])
          #sets old data to the now added data so if it is received again it won't append it
          old_data = new_data
      #calls the graph_make function to display a table every 10 info points, this is only for testing
      if len(btc_time) % 10 == 0:
          graph_make(btc_time, btc_price)
      #waits 5 seconds before trying again so I don't send too many http requests
      time.sleep(5)


def graph_make(btc_time, btc_price):
    pyplot.scatter(btc_time, btc_price)
    pyplot.show()


get_data()
