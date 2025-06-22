def calculate_signal(data: float, strong_sell: float, moderate_sell: float, 
                         neutral: float, moderate_buy: float) -> str:
    """
    this function is used for calculating if data should be treated as a 
    strong/moderate/neutral buy/sell.
    """
    if data <= strong_sell:
        return "Strong Sell"
    elif strong_sell < data <= moderate_sell:
        return "Moderate Sell"
    elif moderate_sell < data <= neutral:
        return "Neutral"
    elif neutral < data <= moderate_buy:
        return "Moderate Buy"
    else:
        return "Strong Buy"
    