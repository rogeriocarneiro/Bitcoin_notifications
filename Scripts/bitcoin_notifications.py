import requests
import time
from datetime import datetime


bitcoin_price_threshold = 200000  # Set this to whatever you like
bitcoin_api_url = 'https://economia.awesomeapi.com.br/last/BTC-BRL'
ifttt_webhook_url = 'https://maker.ifttt.com/trigger/{}/with/key/ctRsGJO0mlPd_wDhnR6zz0'

def get_latest_bitcoin_price():
    resp = requests.get(bitcoin_api_url, verify = False)
    resp_json = resp.json()
    return float(resp_json['BTCBRL']['bid'])

def post_ifttt_webhook(event, value):
    data = {'value1':value}
    ifttt_event_url = ifttt_webhook_url.format(event)
    requests.post(ifttt_webhook_url, json = data, verify = False)

def format_bitcoin_history(bitcoin_history):
    rows =[]
    for i in bitcoin_history:

        date = i['date'].strftime('%d.%m.%Y %H.%M')
        price = i['price']

        row = '{}: $<b>{}</b>'.format(date, price)
        rows.append(row)
        
        #include a breakline between rows
    return '<br>'.join(rows)


def main():
    bitcoin_history = []
    while True:
        price = get_latest_bitcoin_price()
        date = datetime.now()
        bitcoin_history.append({"date":date, "price":price})

        #Send the notification via push notification
        if price < bitcoin_price_threshold:
            post_ifttt_webhook('bitcoin_price_emergency',price)
        
        #Send the notification via sms as setup made at ifttt
        #as long as we have collected the price 5 times
        
        if len(bitcoin_history) == 1:
            post_ifttt_webhook('bitcoin_price_update', format_bitcoin_history(bitcoin_history))
            
            print(f"os valores são {format_bitcoin_history(bitcoin_history)}")        
            #reset the bitcoin_history
            bitcoin_history = []
        
        #sleeps for n minutes
        n = 0.5
        time.sleep(n*60)

if __name__ == '__main__':
    main()