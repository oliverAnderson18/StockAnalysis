import yfinance as yf
import pandas as pd
from Asset import Asset
from Signal import calculate_signal

class Margins():
    """
    We will now create a new class which takes care of a margins analysis
    """
    def __init__(self, asset: Asset):
        self.ticker = asset.ticker
        self.growth = 0
        self.gross_margin = 0
        self.ebit_margin = 0
        self.net_margin = 0
        
        
    def calculate_revenue_growth(self) -> None:
        """
        Calculates the growth of YoY revenue in percentage, which is the growth
        of revenue of an asset in one year.
        """
        tkr = yf.Ticker(self.ticker)
        stmt = tkr.income_stmt
        revenue = stmt.loc["Total Revenue"]
        
        current_revenue = revenue.iloc[0]
        previous_revenue = revenue.iloc[1]
        
        growth = ((current_revenue-previous_revenue)/previous_revenue) * 100 
        self.growth = growth
        
    
    def calculate_gross_margin(self) -> None:
        """
        Calculates the gross_margin of the asset using revenue and gross profit, which represents
        the profitability of a company
        """
        tkr = yf.Ticker(self.ticker)
        stmt = tkr.income_stmt
        revenue = stmt.loc["Total Revenue"]
        gross_profit = stmt.loc["Gross Profit"]
        
        current_revenue = revenue.iloc[0]
        current_profit = gross_profit.iloc[0]
        
        gross_margin = (current_profit/current_revenue) * 100
        self.gross_margin = gross_margin
        
    
    def calculate_EBIT_margin(self) -> None:
        """
        Calculates the earnings before interest
        """
        tkr = yf.Ticker(self.ticker)
        stmt = tkr.income_stmt
        ebit = stmt.loc["EBIT"].iloc[0]
        revenue = stmt.loc["Total Revenue"].iloc[0]
        
        ebit_margin = (ebit/revenue) * 100
        self.ebit_margin = ebit_margin
        
        
    def calculate_net_margin(self) -> None:
        """
        Calculates the net margin of the asset which is the division
        of the net income by the the total revenue.
        """
        tkr = yf.Ticker(self.ticker)
        stmt = tkr.income_stmt
        revenue = stmt.loc["Total Revenue"]
        net_income = stmt.loc["Net Income"]
        
        current_revenue = revenue.iloc[0]
        current_income = net_income.iloc[0]
        
        net_margin = (current_income/current_revenue) * 100
        self.net_margin = net_margin
    
    
    def signals_margin(self) -> list:
        """
        We calculate all margins and estimate if its in a strong/moderate/neutral buy/sell.
        These estimations are not rigid, but are a decent estimate for a mature asset.
        """
        self.calculate_EBIT_margin()
        self.calculate_gross_margin()
        self.calculate_net_margin()
        self.calculate_revenue_growth()
        
        self.signals = [
            calculate_signal(self.growth,
                             -10, 0, 5, 20), 
            calculate_signal(self.gross_margin, 
                             15, 25, 35, 50),
            calculate_signal(self.ebit_margin,
                             0, 6, 12, 20),
            calculate_signal(self.net_margin,
                             0, 5, 10, 20)
        ]
        
        return self.signals
    
    