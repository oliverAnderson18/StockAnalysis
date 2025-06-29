import yfinance as yf
import pandas as pd
import numpy as np
from Asset import Asset
from Signal import calculate_signal

class ValuationMarket():
    """
    We will now create a new class which takes care of the analysis of the valuation and 
    market of an asset.
    """
    def __init__(self, asset: Asset):
        self.ticker = asset.ticker
        self.signals = []
        self.pe = 0
        self.forward_pe = 0
        self.ev = 0
        self.ev_ebitda = 0
        self.ev_sales = 0
        self.fcf = 0
    
    
    def calculate_price_to_earnings(self) -> None:
        """
        We calculate the ratio of price per share divided by the earnings per share ratio.
        This is a good tool to see if an asset is undervalued or overvalued
        """
        tkr = yf.Ticker(self.ticker)
        trailing_pe = tkr.info.get("trailingPE")
        
        self.pe = trailing_pe
        
        
    def calculate_forward_price_to_earnings(self) -> None:
        """
        We do the same as in the price to earnigns ratio, but this time we use the future
        estimated prices of the shares.
        """
        tkr = yf.Ticker(self.ticker)
        forward_pe = tkr.info.get("forwardPE")
        
        self.forward_pe = forward_pe
        
    
    def calculate_ev(self) -> None:
        """
        We calculate enterprise value (ev) by adding market capitalization and total debt, 
        then subtracting cash.This represents the total value of a company as if someone 
        were to buy the entire business.
        """
        tkr = yf.Ticker("AAPL")

        ev = tkr.info.get("enterpriseValue")

        if ev is None:
            market_cap = tkr.info.get("marketCap") or 0
            total_debt = tkr.info.get("totalDebt") or 0
            cash = tkr.info.get("totalCash") or 0
            ev = market_cap + total_debt - cash
        
        self.ev = ev
        
    
    def calculate_ev_ebitda(self) -> None:
        """
        We calculate the ratio of enterprise value divided by EBITDA.
        This is a useful metric to compare companies valuations while 
        adjusting for debt, cash, and differences in capital structure.
        """
        self.calculate_ev()
        
        tkr = yf.Ticker(self.ticker)
        stmt = tkr.income_stmt
        
        ebitda = stmt.loc["EBITDA"].iloc[0]
        
        ev_ebitda = self.ev/ebitda
        
        self.ev_ebitda = ev_ebitda
        
    
    def calculate_ev_sales(self) -> None:
        """
        We calculate the ratio of enterprise value divided by total revenue.
        This helps compare how much investors are paying for each unit of a company’s 
        sales, regardless of profitability.
        """
        self.calculate_ev()
        
        tkr = yf.Ticker(self.ticker)
        revenue = tkr.info.get("totalRevenue")
        
        ev_sales = self.ev/revenue
        self.ev_sales = ev_sales
        
    
    def calculate_free_cash_flow_yield(self) -> None:
        """
        We calculate the free cash flow yield dividing the free cash flow by the market
        capitalization of the asset, multiplied by 100. Overall, it shows the cash the 
        asset is producing compare to the overall value of it
        """
        tkr = yf.Ticker(self.ticker)
        bs = tkr.balance_sheet
        cf = tkr.cash_flow
        
        mket_cap = bs.loc["Total Capitalization"].iloc[0]
        fcf = cf.loc["Free Cash Flow"].iloc[0]
        
        fcf_yield = (fcf/mket_cap) * 100
        
        self.fcf = fcf_yield 
        
    
    def signals_valuation_market(self) -> list:
        """
        We calculate all valuation and market analysis variables and estimate if its 
        in a strong/moderate/neutral buy/sell.These estimations are not rigid, but are 
        a decent estimate for a mature asset.
        """
        self.calculate_ev_ebitda()
        self.calculate_ev_sales()
        self.calculate_price_to_earnings()
        self.calculate_forward_price_to_earnings()
        self.calculate_free_cash_flow_yield()
        
        self.signals = [
            calculate_signal(-self.pe, 
                             -30, -20, -15, -10),
            calculate_signal(-self.forward_pe, 
                             -30, -20, -15, -10),
            calculate_signal(-self.ev_ebitda, 
                             -12, -10, -8, -6),
            calculate_signal(-self.ev_sales, 
                             -5, -3, -2, -1),
            calculate_signal(self.fcf, 
                             1, 3, 5, 8)
        ]
        
        return self.signals
    