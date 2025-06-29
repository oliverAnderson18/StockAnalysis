import yfinance as yf
import pandas as pd
from Asset import Asset
from Signal import calculate_signal


class GrowthPerShare():
    """
    We will now create a class to analyze the growth per share.
    """
    def __init__(self, asset: Asset):
        self.ticker = asset.ticker
        self.signals = []
        self.eps_growth = 0
        self.fcfps = 0
    
    
    def calculate_earnings_per_share_growth(self) -> None:
        """
        Calculates the growth of earnings per share anually, which is the result
        of the division between the difference of the current periods diluted EPS and 
        the last period diluted EPS, divided by last periods diluted EPS and trasnformed into
        a percentage.
        Diluted EPS: Earnings allocated per share after assuming all potential dilutions occur.
        """
        tkr = yf.Ticker(self.ticker)
        stmt = tkr.income_stmt
        eps = stmt.loc["Diluted EPS"]
        
        current_eps = eps.iloc[0]
        previous_eps = eps.iloc[1]
        
        eps_growth = (current_eps-previous_eps)/previous_eps * 100
        self.eps_growth = eps_growth
        
    
    def calculate_free_cash_flow_per_share_growth(self) -> None:
        """
        Calculates the amount of free cash flow per share, which is used as a proxy
        to measure the changes in earnings per share. This is the result of dividing the 
        free cash flow an asset has by the amount of shares. 
        """
        tkr = yf.Ticker(self.ticker)
        stmt = tkr.income_stmt
        
        free_cash_flow = tkr.cash_flow.loc["Free Cash Flow"]
        basic_avg_shares = stmt.loc["Basic Average Shares"]
        
        current_fcf = free_cash_flow.iloc[0]
        previous_fcf = free_cash_flow.iloc[1]
        
        current_bas = basic_avg_shares.iloc[0]
        previous_bas = basic_avg_shares.iloc[1]
        
        current_fcfps = current_fcf/current_bas
        previous_fcfps = previous_fcf/previous_bas
        
        fcfps_growth = (current_fcfps-previous_fcfps)/previous_fcfps * 100
        self.fcfps = fcfps_growth
        
    
    def signals_growth_per_action(self) -> list:
        """
        We calculate all growth per stock variables and estimate if its in a 
        strong/moderate/neutral buy/sell.These estimations are not rigid, but are 
        a decent estimate for a mature asset.
        """
        self.calculate_earnings_per_share_growth()
        self.calculate_free_cash_flow_per_share_growth()
        
        self.signals = [
            calculate_signal(self.eps_growth, 
                             -10, 0, 8, 20),
            calculate_signal(self.fcfps,
                             -5, 0, 7, 15)
        ]
        
        return self.signals
        
        