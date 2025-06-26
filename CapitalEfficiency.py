import yfinance as yf
import pandas as pd
import numpy as np
from Asset import Asset
from Signal import calculate_signal

class CapitalEfficiency():
    """
    We will now create a new class which takes care of the analysis of capital efficiency.
    """
    def __init__(self, asset: Asset):
        self.ticker = asset.ticker
        self.signals = []
        self.ROIC = 0
        self.WACC = 0
        self.spread = 0
        self.ROE = 0
        self.AT = 0
        
    
    def calculate_ROIC(self) -> None:
        """
        ROIC: Return On Invested capitals.
        After-tax operating profit divided by invested capital;
        indicates efficiently a company generates returns on resources.
        """
        tkr = yf.Ticker(self.ticker)
        inc = tkr.income_stmt.T.iloc[:3]
        bal = tkr.balance_sheet.T.iloc[:3]

        roics = []
        for idx in inc.index:
            stmt = inc.loc[idx]
            bs = bal.loc[idx]
            
            ebit = stmt.loc["EBIT"] # Earnings before interests and tax
            tax_rate = stmt.loc["Tax Provision"]/stmt.loc["Pretax Income"]
            nopat = ebit * (1-tax_rate) # Net operating profit after tax
            
            equity = bs.loc["Common Stock Equity"]
            debt = bs.loc["Total Debt"]
            
            # Now we calculate an aproximate of all cash that is not truly invested.
            cash = (bs.loc["Cash Cash Equivalents And Short Term Investments"] +
                bs.loc["Other Short Term Investments"])
            
            invested_capital = equity + debt - cash
            
            roics.append(nopat / invested_capital)
        
        self.ROIC = sum(roics) / len(roics)
        
        
    def calculate_WACC(self) -> None:
        """
        WACC: Weighted-Average Cost of Capital.
        Blended after-tax cost of equity and debt; 
        baseline return projects require for positive value creation.
        """
        tkr = yf.Ticker(self.ticker)
        inc = tkr.income_stmt.T.iloc[:3]
        bal = tkr.balance_sheet.T.iloc[:3]

        mkt_cap = tkr.fast_info["marketCap"]

        beta = tkr.info.get("beta", 1) 
        """
        This gives the beta value (how correlated risk is of the asset is with 
        the market) and gives a fall back of 1 (assume same risk).
        """
        risk_free = 0.042 # Estimated value, not exact, based on 10 year treasury
        equity_risk_premium = 0.05 # Estimated value, not exact, based on USA/Europe stocks
        
        cost_equity = risk_free + equity_risk_premium * beta # CAPM

        waccs = []
        for idx in inc.index:
            stmt = inc.loc[idx]
            bs = bal.loc[idx]

            debt = bs.loc["Total Debt"]
            total_cap = mkt_cap + debt
            equity_weight = mkt_cap / total_cap
            debt_weight = debt / total_cap

            interest_expense = stmt.loc["Interest Expense"]
            cost_debt = abs(interest_expense) / debt
            tax_rate = stmt.loc["Tax Provision"] / stmt.loc["Pretax Income"]
            cost_debt_after_tax = cost_debt * (1 - tax_rate)

            waccs.append(equity_weight * cost_equity + debt_weight * cost_debt_after_tax)

        self.WACC = sum(waccs) / len(waccs)
        
    
    def calculate_spread(self) -> None:
        """
        Difference between returns earned on invested capital and capital's cost; 
        measures value creation or destruction.
        """
        self.calculate_ROIC()
        self.calculate_WACC()
        
        spread = self.ROIC - self.WACC
        self.spread = spread
        
    def calculate_ROE(self) -> None:
        """
        Results of the division between the net income of an asset divided by the equity.
        ROE measures the efficiency of the investments made with the shareholders investments.
        """
        tkr = yf.Ticker(self.ticker)
        stmt = tkr.income_stmt
        bs = tkr.balancesheet
        
        equity = bs.loc["Common Stock Equity"].iloc[0]
        net_income = stmt.loc["Net Income"].iloc[0]
        
        ROE = (net_income/equity) * 100
        self.ROE = ROE
    
    
    def calculate_asset_turnover(self) -> None:
        """
        We calculate all revenue and divide it by the total of assets. This is 
        used for measuring how efficiently a company uses its assets to generate sells.
        """
        tkr = yf.Ticker(self.ticker)
        stmt = tkr.income_stmt
        bs = tkr.balance_sheet
        
        revenue = stmt.loc["Total Revenue"].iloc[0]
        assets = bs.loc["Total Assets"].iloc[0]
        
        asset_turnover = revenue/assets
        self.AT = asset_turnover
            
        
        
    def signals_capital_efficiency(self) -> list:
        """
        We calculate all capital efficiency variables and estimate if its in a 
        strong/moderate/neutral buy/sell.These estimations are not rigid, but are 
        a decent estimate for a mature asset.
        """
        self.calculate_spread()
        self.calculate_ROE()
        self.calculate_asset_turnover()
        
        self.signals = [
             calculate_signal(self.spread,
                              -10, -3, 3, 10),
             calculate_signal(self.ROE, 
                              5, 10, 15, 20),
             calculate_signal(self.AT,
                              0.25, 0.5, 1, 2)
             
        ]
        
        return self.signals
        