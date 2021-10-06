import requests
import time
from datetime import datetime


# Thresholds to be considered in the emergency notification
BITCOIN_LOW_PRICE_THRESHOLD = 200000
BITCOIN_HIGH_PRICE_THRESHOLD = 300000


# URL from where the BTC price is gotten from
BITCOIN_API_URL = 'https://economia.awesomeapi.com.br/last/BTC-BRL'

# It's the base URL to use the webhook API of IFTTT
IFTTT_WEBHOOKS_URL = 'https://maker.ifttt.com/trigger/{}/with/key/{}'

# The key below is obtained at the documentation page of the IFTTT webhook documentation.
IFTTT_KEY = input("What's your IFTTT key?")

# This function obtains the last BTC price (in BRL values) through the API provided above.
def get_latest_bitcoin_price():
    response = requests.get(BITCOIN_API_URL, verify = False)
    response_json = response.json()
    return float(response_json['BTCBRL']['bid'])  # Converts the price to a floating point number

# This function sends a post request to the webhook URL
def post_ifttt_webhook(event, value):
    data = {'value1': value}  # The payload that will be sent to IFTTT service
    ifttt_event_url = IFTTT_WEBHOOKS_URL.format(event, IFTTT_KEY)  # Inserts our desired event
    requests.post(ifttt_event_url, json=data, verify = False)

# This function formats the raw btc value and timestamp
def format_bitcoin_history(bitcoin_history):
    rows = []
    for bitcoin_price in bitcoin_history:
        # Formats the date into a string: '24/02 15:09'
        date = bitcoin_price['date'].strftime('%d/%m %H:%M')
        price = bitcoin_price['price']

        # <b> (bold) tag creates bolded text
        row = '{}: $<b>{:,.0f}</b>'.format(date, price)  # 24/02 15:09: $<b>101,234</b>
        rows.append(row)

    # A <br> (break) creates a new line
    return '<br>'.join(rows)  # Join the rows delimited by <br> tag: row1<br>row2<br>row3

def main():
    bitcoin_history = []
    while True:
        price = get_latest_bitcoin_price()
        date = datetime.now()
        bitcoin_history.append({'date': date, 'price': price})

        # Send an emergency notification
        if (price < BITCOIN_LOW_PRICE_THRESHOLD) or (price >BITCOIN_HIGH_PRICE_THRESHOLD):
            post_ifttt_webhook('bitcoin_price_emergency', price)

        # Send a Telegram notification
        if len(bitcoin_history) == 5:  # Once we have 5 items in our bitcoin_history send an update
            post_ifttt_webhook('bitcoin_price_update', format_bitcoin_history(bitcoin_history))
            # Reset the history
            bitcoin_history = []

        n = 5
        time.sleep(n * 60)  # Sleep for n minutes (for testing purposes you can set it to a lower number)

if __name__ == '__main__':
    main()
