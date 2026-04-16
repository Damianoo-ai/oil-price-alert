import requests
import os


def shorten_url(link):
    
    if link is None:
        print('BITLY: Url not found')
        return None
    
    bitly_header = {
        "Authorization": f"Bearer {os.getenv('BITLY_TOKEN')}",
        "Content-Type": "application/json"
    }
    
    payload = {
        'long_url': link,
    }

    try:
        response = requests.post(
            url='https://api-ssl.bitly.com/v4/shorten',
            headers=bitly_header,
            json=payload,
            timeout=5
        )
        
    except requests.exceptions.Timeout as e:
        print(f'BITLY Timeout overcomed')
    except requests.exceptions.ConnectionError as e:
        print(e)
        return None
    except requests.exceptions.RequestException as e:
        print(e)
        return None
    except Exception as e:
        print(e)
        return None
    
        
    if response.status_code not in (201,200):
        print(f'BITLY HTTP Error: {response.status_code}{response.text}')
        return None
    
    try:
        data:dict = response.json()
    except ValueError as e:
        print(f'Invalid JSON {e}')
        return None
    
    link = data.get('link')

    if not link:
        print('BITLY: link not present in the response')
        return None
    
    return link