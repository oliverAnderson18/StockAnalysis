import yfinance as yf
import pandas as pd
import numpy as np
from Asset import Asset
from Signal import calculate_signal

class SolvencyLiquidity():
    """
    We will now create a new class which takes care of the analysis of the solvency and 
    liquidity of an asset.
    """
    def __init__(self, asset: Asset):
        self.ticker = asset.ticker
        self.signals = []
        self.NDEBITDA_ratio = 0
        self.interest_coverage = 0
        self.current_ratio = 0
    
    
    def calculate_net_debt_to_EBITDA_ratio(self) -> None:
        """
        We calculate the net debt to EBITDA ratio diving the net debt by the EBITDA, which is 
        a measure for the company's profitabilty excluding debt, taxes, depreciation and amortization.
        This ratio indicates how long it would take to pay off its debt using EBITDA. 
        """
        tkr = yf.Ticker(self.ticker)
        stmt = tkr.income_stmt
        bs = tkr.balance_sheet
        
        ebitda = stmt.loc["EBITDA"].iloc[0]
            
        # Now we calculate an aproximate of all cash that is not truly invested.
        cash = (bs.loc["Cash Cash Equivalents And Short Term Investments"].iloc[0] +
            bs.loc["Other Short Term Investments"].iloc[0])
        
        debt = bs.loc["Total Debt"].iloc[0]
        
        net_debt = debt - cash
        
        ratio = net_debt/ebitda
        
        self.NDEBITDA_ratio = ratio
        
    
    def calculate_interest_coverage(self) -> None:
        """
        We calculate the interest coverage by diving the EBIT by the interest expense.
        EBIT measures the earnings before interests and taxes, and the interest expense measures
        the cost of borrowing money. The interest coverage measures how easily a company can
        pay interest.
        """
        tkr = yf.Ticker(self.ticker)
        stmt = tkr.income_stmt
        
        ebit = None
        interest_expense = None
        
        # Sometimes we must use data from 2 years ago due to NaN values
        
        for i in range(2):
            try:
                ebit_candidate = stmt.loc["EBIT"].iloc[i]
                expense_candidate = stmt.loc["Interest Expense"].iloc[i]

                if pd.notna(ebit_candidate) and pd.notna(expense_candidate) and expense_candidate != 0:
                    ebit = ebit_candidate
                    interest_expense = expense_candidate
                    break
            except (KeyError, IndexError):
                continue  # Try next period

        if ebit is None or interest_expense is None:
            print("Could not calculate interest coverage ratio due to missing data. Therefore we asume an average interest expense of 4")
            self.interest_coverage = 4
            return

        interest_coverage = ebit / interest_expense
        self.interest_coverage = interest_coverage
        
    
    def calculate_current_ratio(self) -> None:
        """
        We calculate the current ratio by dividing the current assets by the current
        liabilities. This measures a company's ability to pay off its short term liabilities.
        """
        tkr = yf.Ticker(self.ticker)
        bs = tkr.balance_sheet
        
        assets = bs.loc["Current Assets"].iloc[0]
        liabilites = bs.loc["Current Liabilities"].iloc[0]
        
        current_ratio = assets/liabilites
        self.current_ratio = current_ratio
        
    
    def calculate_signal_current_ratio(self) -> None:
        """
        The current ratio works a different from the other variables, 
        so we have to create our own function to analyze what signal
        it gives us.
        """
        self.calculate_current_ratio()
        
        if self.current_ratio < 1:
            return "Strong Sell"
        elif self.current_ratio < 1.5:
            return "Neutral"
        elif self.current_ratio < 2:
            return "Moderate Buy"
        elif self.current_ratio < 3:
            return "Strong Buy"
        elif self.current_ratio > 3:
            return "Moderate Sell"
    
    
    def signals_solvency_liquidity(self) -> list:
        """
        We calculate all solvency and liquidity analysis variables and estimate if its 
        in a strong/moderate/neutral buy/sell.These estimations are not rigid, but are 
        a decent estimate for a mature asset.
        """
        self.calculate_net_debt_to_EBITDA_ratio()
        self.calculate_interest_coverage()
        
        self.signals = [
             calculate_signal(-self.NDEBITDA_ratio,
                              -4, -3, -2, -1),
             calculate_signal(self.interest_coverage,
                              1.5, 3, 5, 8),
             self.calculate_signal_current_ratio()
        ]
        
        return self.signals
    