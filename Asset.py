import yfinance as yf
import pandas as pd

class Asset:
    
    def __init__(self, ticker: str, areas: list):
        self.ticker = ticker.upper()
        self.areas = areas
        self.point = 0
        self.final_signal = ""
        