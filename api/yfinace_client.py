# Change the value if needed
SELECTED_TICKER = {
    'BZ=F': 'Brent Crude'
}

import time
import yfinance as yf

class Yfinance_Client:
    def __init__(self):
        self.df = None
        self.ticker = None
        self.positive_delta = False
        self.today_price = 0.00
        self.yesterday_price = 0.00
        self.percent_change = 0.00
        
    def fetch_data(self, attempts, delay):
        self.ticker = list(SELECTED_TICKER.keys())[0]

        self.df = None
        for attempt in range(1, attempts+1):
            try:
                brent = yf.Ticker(self.ticker)
                self.df = brent.history(period="5d")
            except Exception as e:
                print(f'Yahoo finance ERROR:\n {e}')
                self.df = None
            
            if self.df is not None and not self.df.empty:
                break
            
            print(f"Retry {attempt}/{attempts}")
            time.sleep(delay)
            
        if self.df is None or self.df.empty:
            raise RuntimeError("Yahoo Finance returned empty dataframe")
        else:
            if self.df['Close'].isna().any():
                print('NaN values present')
        
        return self.df

    def percent_price(self):
        if self.df is None:
            raise RuntimeError("Data not fetched yet")
        
        self.positive_delta = False
        
        self.today_price = self.df["Low"].iloc[-1]
        self.yesterday_price = self.df["Low"].iloc[-2]
        if self.yesterday_price == 0:
            raise RuntimeError("Invalid previous price (0)")
        
        delta_price = self.today_price - self.yesterday_price
        if delta_price > 0:
            self.positive_delta = True
        
        self.percent_change = (delta_price / self.yesterday_price) * 100
        return self.percent_change

    def choose_symbol(self):
        return '🔺' if self.positive_delta else '🔻'
            
            
    def print_diff(self):
        print(f'{self.df.index[-1]}:  {round(self.today_price, 2)}')
        print(f'{self.df.index[-2]}:  {round(self.yesterday_price, 2)}')
        print(f'Price change: {self.choose_symbol()}{round(self.percent_change, 2)}%')
        