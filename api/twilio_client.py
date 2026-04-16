from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
import os
from api.bitly_client import shorten_url



def build_body_sms(article, symbol, asset_name, percent_chg, short_url)->str:
    
    title = article.get('title')
        
    if not title:
            title = 'Untitled news'
            
    return (
        f"{asset_name}: {symbol}{round(percent_chg, 2)}%\n"
        f"{title}\n"
        f"{short_url or ''}"
    )
            
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
        
        
        