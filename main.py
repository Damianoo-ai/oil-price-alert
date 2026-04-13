from news_sender import NewsSender
import yfinance as yf
from twilio.rest import Client
import os
import requests
from dotenv import load_dotenv

load_dotenv()  

# Change the value if needed
SELECTED_TICKER = {
    'BZ=F': 'Brent Oil'
}

ns = NewsSender()
ticker = list(SELECTED_TICKER.keys())[0]
brent = yf.Ticker(ticker)
df = brent.history(period="5d")

print(df)

# Find the increase/decrease of the price
positive_delta = False
today_price = df["Close"].iloc[-1]
yest_price = df["Close"].iloc[-2]
delta_price = today_price - yest_price
if delta_price > 0:
    positive_delta = True

symbol = "🔺" if positive_delta else '🔻'
percent_price = (delta_price / yest_price) * 100

print(f'{df.index[-1]}:  {round(today_price, 2)}')
print(f'{df.index[-2]}:  {round(yest_price, 2)}')
print(f'Price change: {symbol}{round(percent_price, 2)}%')

# Create the news, filter and save in a file
data = ns.create_news()
filtered = ns.filter_news(data)
saved = ns.save_news(filtered)
print(f'Atleast one news? {saved}Total News:{ns.count_news}')


if abs(percent_price) >= 5:
    client = Client(os.getenv('TWILIO_ACCOUNT_SID'), os.getenv('TWILIO_AUTH_TOKEN'))

    for art in filtered:
        bitly_header = {
            "Authorization": f"Bearer {os.getenv('BITLY_TOKEN')}",
            "Content-Type": "application/json"
        }
        bitly_par = {
            'long_url': art['url'],
        }

        short_url = requests.post(
            url='https://api-ssl.bitly.com/v4/shorten',
            headers=bitly_header,
            json=bitly_par
        )
        
        if short_url.status_code not in (201,200):
            short_url = None

        message = client.messages.create(
            body=(
                f"{SELECTED_TICKER[ticker]}: {symbol}{round(percent_price, 2)}%\n"
                f"{art['title']}\n"
                f"{short_url.json()['link'] if short_url else ''}"
            ),
            from_=os.getenv('TWILIO_TRIAL_NUMBER'),
            to=os.getenv('TEST_NUMBER')
        )

        print(message.status)