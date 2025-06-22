import yfinance as yf
import pandas as pd
from Asset import Asset
from Signal import calculate_signal


class GrowthPerAction():
    """
    We will now create a class to analyze the growth per action.
    """
    def __init__(self, asset: Asset):
        self.ticker = asset.ticker
    