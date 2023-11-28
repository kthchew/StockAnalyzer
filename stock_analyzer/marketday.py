import time


class MarketDay:
    """A class that represents a single data point."""
    def __init__(self, date_string, open_price, high, low, close, vol, dividends, ticker, industry, country):
        self.date = time.strptime(date_string, "%Y-%m-%d %H:%M:%S%z")
        self.open = open_price
        self.high = high
        self.low = low
        self.close = close
        self.vol = vol
        self.dividends = dividends
        self.ticker = ticker
        self.industry = industry
        self.country = country

    def __lt__(self, other):
        return self.date < other.date

    def __le__(self, other):
        return self.date <= other.date
