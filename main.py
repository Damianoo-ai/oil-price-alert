
import os
from dotenv import load_dotenv
from api.news_client import *
from api.yfinace_client import *
from api.twilio_client import send_sms

load_dotenv()  

yfc = Yfinance_Client()
yfc.fetch_data(attempts=4, delay=3)
print(yfc.df)

# Find the increase/decrease of the price
yfc.percent_price()

#Print the difference
yfc.print_diff()

# Create the news, filter and save in a file
data = create_news()
filter_news = filter_news(data)
saved = save_news(filter_news)
print(f'Atleast one news? {saved}\nTotal News:{len(data)}')


if abs(yfc.percent_change) >= 5:
    
    send_sms(
        news=filter_news,
        symbol=yfc.choose_symbol(),
        asset_name=SELECTED_TICKER[yfc.ticker],
        percent_chg=yfc.percent_change
    )
    
    # print(message.status)