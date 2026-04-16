from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
import os
from api.bitly_client import shorten_url
from news_client import PRICE_MOVEMENT_KEYWORD
#Max lenght of the sms message(Impose by Twilio)
MAX_LENGHT_SMS = 160

def build_body_sms(article, symbol, asset_name, percent_chg, short_url)->str:
    
    title = article.get('title') or 'Untitled news'    
    new_title = title
    
    fixed_test = (f"{asset_name}: {symbol}{round(percent_chg, 2)}%\n\n{short_url or ''}")
    
    remaining = MAX_LENGHT_SMS - len(fixed_test) 
    if (remaining < 0):
        
        if(abs(remaining)>len(title)):
            keyword_news = ''
            word_in_title = [w.lower() for w in title.split()]
            for k in PRICE_MOVEMENT_KEYWORD:
                if k in word_in_title:
                    keyword_news = k
                    break
                
            new_title = f'{keyword_news.title()} on the market' if keyword_news else 'Market news'
        else:
            new_len = max(0, remaining - 3)
            new_title = title[:new_len] + '...'
            
    final_text = (f"{asset_name}: {symbol}{round(percent_chg, 2)}%\n{new_title}\n{short_url or ''}")

    return final_text
    
            
def send_sms(news:list[dict],symbol, asset_name, percent_chg):
    
    client = Client(os.getenv('TWILIO_ACCOUNT_SID'), os.getenv('TWILIO_AUTH_TOKEN'))

    for art in news:
        try:
            s_link = shorten_url(link=art['url'])
            
            text = build_body_sms(art,symbol, asset_name, percent_chg, s_link)
            
            response = client.messages.create(
                body=text,
                from_=os.getenv('TWILIO_TRIAL_NUMBER'),
                to=os.getenv('TEST_NUMBER')
            )
            print(f"[OK] SID={response.sid}, status={response.status}")
                
        except TwilioRestException as e:
            print(f"[TWILIO ERROR] code={e.code} msg={e.msg}")
        except Exception as e:
            print(f'[Generic Error]: {e}')
        
        
        