from Asset import Asset
from CapitalEfficiency import CapitalEfficiency
from Margins import Margins
from GrowthPerShare import GrowthPerShare
from SolvencyLiquidity import SolvencyLiquidity
from ValuationMarket import ValuationMarket
from Signal import *

asset_ticker = input("Please introduce the ticker of the asset you want to analyze: ")

print("We calculate the signal using different fields, being these fields:")
print("1-Growth per share: Measures how a company’s earnings or cash flow per share increase over time, indicating performance.")
print("2-Capital Efficiency: Measures capital efficiency by calculating returns, cost of capital, and asset use to assess investment quality.")
print("3-Margins: Analyzes profitability by calculating revenue growth, gross, EBIT, and net margins to assess financial health.")
print("4-Solvency Liquidity: Analyzes a company’s ability to pay debts and short-term liabilities using debt and liquidity ratios.")
print("5-Valuation Market: Analyzes asset valuation using P/E ratios, enterprise value multiples, and free cash flow yield metrics.")

print("Choose which options you would like to have analyzed (can be all). Indicate them by the numbers next to the name, separting by commas.")

areas_list = list(input("Insert the options: "))

areas = [int(x) for x in areas_list if x.isdigit()]

asset = Asset(asset_ticker, areas)

def calculate_total_points(asset) -> None:
    """
    We calculate the final point depending on the areas the user has chosen to be analyzed.
    """
    total_points_sum = 0
    total_signals_analyzed = 0

    if 1 in asset.areas:
        gps = GrowthPerShare(asset)
        gps.signals_growth_per_action()
        
        for signal in gps.signals:
            total_points_sum += calculate_signal_points(signal)
            total_signals_analyzed += 1
                
    if 2 in asset.areas:
        ce = CapitalEfficiency(asset)
        ce.signals_capital_efficiency()
       
        for signal in ce.signals:
            total_points_sum += calculate_signal_points(signal)
            total_signals_analyzed += 1
                
    if 3 in asset.areas:
        m = Margins(asset)
        m.signals_margin()
            
        for signal in m.signals:
            total_points_sum += calculate_signal_points(signal)
            total_signals_analyzed += 1
                
    if 4 in asset.areas:
        sl = SolvencyLiquidity(asset)
        sl.signals_solvency_liquidity()
            
        for signal in sl.signals:
            total_points_sum += calculate_signal_points(signal)
            total_signals_analyzed += 1
                
    if 5 in asset.areas:
        vm = ValuationMarket(asset)
        vm.signals_valuation_market()
            
        for signal in vm.signals:
            total_points_sum += calculate_signal_points(signal)
            total_signals_analyzed += 1
        
    if total_signals_analyzed == 0:
        asset.point = 0
        
    else:
        asset.point = total_points_sum/total_signals_analyzed
        
    
def calculate_signal(asset) -> None:
    """
    We will transform the total points to signals
    """
    calculate_total_points(asset)
    
    asset.final_signal = calculate_points_to_signal(asset.point)
    
    
calculate_signal(asset)
    
print("")
print(asset.final_signal)
            