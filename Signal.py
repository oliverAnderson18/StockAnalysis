import math


def calculate_signal(data: float, strong_sell: float, moderate_sell: float, 
                         neutral: float, moderate_buy: float) -> str:
    """
    This function is used for calculating if data should be treated as a 
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
    

def calculate_signal_points(signal: str) -> int:
    """
    We calculate the points awarded to a signal.
    """
    if signal == "Stron Sell":
        return -2
    elif signal == "Moderate Sell":
        return -1
    elif signal == "Neutral":
        return 0
    elif signal == "Moderate Buy":
        return 1
    else:
        return 2
    

import math

def calculate_points_to_signal(points: float) -> str:
    floor_val = math.floor(points)
    ceil_val = math.ceil(points)

    dist_floor = points - floor_val
    dist_ceil = ceil_val - points

    if dist_floor <= dist_ceil:
        assigned_signal = floor_val
        percent = int((1 - dist_floor) * 100)
    else:
        assigned_signal = ceil_val
        percent = int((1 - dist_ceil) * 100)

    signals_map = {
        2: "Strong Buy",
        1: "Moderate Buy",
        0: "Neutral",
        -1: "Moderate Sell",
        -2: "Strong Sell"
    }

    signal_text = signals_map.get(assigned_signal, "Strong Sell")

    return f"{percent}% {signal_text}"

