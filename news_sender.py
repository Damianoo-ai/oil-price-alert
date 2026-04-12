import os 
from dotenv import load_dotenv
from datetime import datetime as dt, timedelta
import json
import requests

PRICE_MOVEMENT_KEYWORD = [
    'spike',
    'jump',
    'drop',
    'surge',
    'surged',
    'jumped',
    'dropped',
    'fell',
    'decline',
    'crash'
]
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"


class NewsSender:
    def __init__(self):
         self.count_news = 0

    def create_news(self):
        
            load_dotenv()

            now = dt.now()
            two_days_ago = now - timedelta(days=2)

            parameters={
                    'apiKey': os.getenv('NEWS_API_KEY'),
                    'language': 'en',
                    'q': '''
                    (oil OR "crude oil" OR brent OR WTI)
                    AND
                    ("price surge" OR "price spike" OR "price jump" OR "price drop" OR "price fall" OR "price slump"
                    OR OPEC OR "production cut" OR sanctions OR war OR "supply disruption")
                    ''',
                    'sortBy': 'publishedAt',
                    'searchIn': 'title',
                    'from': two_days_ago.strftime("%Y-%m-%d"),
                    'to': now.strftime('%Y-%m-%d')
                }

            resp = requests.get(url=NEWS_ENDPOINT,params=parameters)
            data:dict = resp.json()

            return data

    def filter_news(self, articles: dict):

        filtered_list = []
        for art in articles['articles']:
            title = art['title']
            if title is None:
                continue
            title = title.lower()

            for keyword in PRICE_MOVEMENT_KEYWORD:
                if keyword in title:
                    filtered_list.append(art)
                    break
        return filtered_list[:3]
            
    def save_news(self,articles_list):
          if len(articles_list) > 0:
            with open('./news_data.json','w') as writer:
                    writer.write(json.dumps(articles_list,indent=2))
            return True
          return False