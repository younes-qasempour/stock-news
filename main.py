import requests
from data import *
from twilio.rest import Client


STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"
STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"


parameters = {
    'function': 'TIME_SERIES_DAILY',
    'symbol': STOCK_NAME,
    'outputsize': 'compact',
    'apikey': ALPHA_VANTAGE_API_KEY,
}

response = requests.get(STOCK_ENDPOINT, params=parameters)
response.raise_for_status()
stock_data = response.json()['Time Series (Daily)']
closing_prices = [value['4. close'] for (key, value) in stock_data.items()]

yesterday_closing_price = float(closing_prices[0])
day_before_yesterday_closing_price = float(closing_prices[1])
closing_price_difference = yesterday_closing_price - day_before_yesterday_closing_price
up_down = None
if closing_price_difference > 0:
    up_down = '🔺'
else:
    up_down = '🔻'
closing_price_difference_percentage = round(closing_price_difference / yesterday_closing_price * 100)

if abs(closing_price_difference_percentage) >= 4:
    new_parameters = {
        'qInTitle': COMPANY_NAME,
        'apikey': NEWS_API_KEY,
    }
    response = requests.get(NEWS_ENDPOINT, params=new_parameters)
    response.raise_for_status()
    news_data = response.json()['articles']
    three_articles = news_data[:3]
    messages_list = [(f"{STOCK_NAME}: {up_down}{closing_price_difference_percentage}%\nHeadline: {article['title']}."
                      f" \nBrief: {article['description']}") for article in three_articles]

    client = Client(ACCOUNT_SID, AUTH_TOKEN)
    for article in messages_list:
        message = client.messages.create(
            from_='+18506652594',
            to=PHONE_NUMBER,
            body=f'{article}'
        )
