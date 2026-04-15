from news_sender import NewsSender
import yfinance as yf
from twilio.rest import Client
import os
from dotenv import load_dotenv
from url_manager import shorten_url
import time


load_dotenv()  

# Change the value if needed
SELECTED_TICKER = {
    'BZ=F': 'Brent Crude'
}

ns = NewsSender()
ticker = list(SELECTED_TICKER.keys())[0]

df = None
for attempt in range(3):
    try:
        brent = yf.Ticker(ticker)
        df = brent.history(period="5d")
    except Exception as e:
        print(f'Yahoo finance ERROR:\n {e}')
        df = None
    
    if df is not None or not df.empty:
        break
    
    print(f"Retry {attempt + 1}/3")
    time.sleep(2)
    
if df.empty or df is None:
    print("Empty dataframe")
else:
    if df['Close'].isna().any():
        print('NaN values present')

print(df)
# Find the increase/decrease of the price
positive_delta = False
today_price = df["Low"].iloc[-1]
yest_price = df["Low"].iloc[-2]
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
filter_news = ns.filter_news(data)
saved = ns.save_news(filter_news)
print(f'Atleast one news? {saved}\nTotal News:{ns.count_news}')


if abs(percent_price) >= 5:
    client = Client(os.getenv('TWILIO_ACCOUNT_SID'), os.getenv('TWILIO_AUTH_TOKEN'))

    for art in filter_news:

        s_link = shorten_url(link=art['url'])
        
        message = client.messages.create(
            body=(
                f"{SELECTED_TICKER[ticker]}: {symbol}{round(percent_price, 2)}%\n"
                f"{art['title']}\n"
                f"{s_link.json()['link'] if s_link else ''}"
            ),
            from_=os.getenv('TWILIO_TRIAL_NUMBER'),
            to=os.getenv('TEST_NUMBER')
        )

        print(message.status)