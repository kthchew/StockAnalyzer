import time


class MarketDay:
    """A class that represents a single data point."""

    def __init__(self, date_string, open_price, high, low, close, vol, dividends, splits, ticker, industry, country):
        self.date = time.strptime(date_string, "%Y-%m-%d %H:%M:%S%z")
        self.open = float(open_price)
        self.high = float(high)
        self.low = float(low)
        self.close = float(close)
        self.vol = float(vol)
        self.dividends = float(dividends)
        self.splits = float(splits)
        self.ticker = ticker
        self.industry = industry
        self.country = country

    def __lt__(self, other):
        return self.date < other.date

    def __le__(self, other):
        return self.date <= other.date

    def __eq__(self, other):
        if isinstance(other, MarketDay):
            return (self.date == other.date and
                    self.open == other.open and
                    self.high == other.high and
                    self.low == other.low and
                    self.close == other.close and
                    self.vol == other.vol and
                    self.dividends == other.dividends and
                    self.splits == other.splits and
                    self.ticker == other.ticker and
                    self.industry == other.industry and
                    self.country == other.country)
        return False
