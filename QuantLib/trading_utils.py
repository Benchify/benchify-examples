import numpy as np
import pandas as pd
from typing import Union, List, Dict, Tuple, Optional
import time
from datetime import datetime, timedelta

def calculate_vwap(prices: List[float], volumes: List[int]) -> float:
    """Calculate Volume Weighted Average Price."""
    return sum(p * v for p, v in zip(prices, volumes)) / sum(volumes)

def calculate_twap(prices: List[float], timestamps: List[int]) -> float:
    """Calculate Time Weighted Average Price."""
    if len(prices) <= 1:
        return prices[0] if prices else 0
    
    weights = []
    for i in range(1, len(timestamps)):
        weights.append(timestamps[i] - timestamps[i-1])
    
    total_weight = sum(weights)
    return sum(p * w / total_weight for p, w in zip(prices[1:], weights))

def calculate_ema(data: List[float], span: int) -> List[float]:
    """Calculate Exponential Moving Average."""
    alpha = 2 / (span + 1)
    ema = [data[0]]
    
    for i in range(1, len(data)):
        ema.append(alpha * data[i] + (1 - alpha) * ema[i-1])
    
    return ema

def calculate_bollinger_bands(data: List[float], window: int = 20, num_std: float = 2.0) -> Tuple[List[float], List[float], List[float]]:
    """Calculate Bollinger Bands - returns (upper_band, middle_band, lower_band)."""
    middle_band = calculate_sma(data, window)
    
    rolling_std = []
    for i in range(len(data)):
        if i < window - 1:
            rolling_std.append(np.std(data[:i+1]))
        else:
            rolling_std.append(np.std(data[i-window+1:i+1]))
    
    upper_band = [m + (s * num_std) for m, s in zip(middle_band, rolling_std)]
    lower_band = [m - (s * num_std) for m, s in zip(middle_band, rolling_std)]
    
    return upper_band, middle_band, lower_band

def calculate_sma(data: List[float], window: int) -> List[float]:
    """Calculate Simple Moving Average."""
    result = []
    for i in range(len(data)):
        if i < window - 1:
            result.append(sum(data[:i+1]) / (i+1))
        else:
            result.append(sum(data[i-window+1:i+1]) / window)
    return result

def calculate_rsi(data: List[float], window: int = 14) -> List[float]:
    """Calculate Relative Strength Index."""
    deltas = [data[i] - data[i-1] for i in range(1, len(data))]
    
    # Prepend a zero to match original data length
    seed = [0]
    up = seed + [delta if delta > 0 else 0 for delta in deltas]
    down = seed + [-delta if delta < 0 else 0 for delta in deltas]
    
    # Calculate RS using exponential moving averages
    up_ema = calculate_ema(up, window)
    down_ema = calculate_ema(down, window)
    
    rs = [0 if d == 0 else u/d for u, d in zip(up_ema, down_ema)]
    rsi = [100 - 100 / (1 + r) for r in rs]
    
    return rsi

def calculate_macd(data: List[float], fast_span: int = 12, slow_span: int = 26, signal_span: int = 9) -> Tuple[List[float], List[float], List[float]]:
    """Calculate MACD, Signal Line, and Histogram."""
    fast_ema = calculate_ema(data, fast_span)
    slow_ema = calculate_ema(data, slow_span)
    
    macd_line = [f - s for f, s in zip(fast_ema, slow_ema)]
    signal_line = calculate_ema(macd_line, signal_span)
    histogram = [m - s for m, s in zip(macd_line, signal_line)]
    
    return macd_line, signal_line, histogram

def calculate_sharpe_ratio(returns: List[float], risk_free_rate: float = 0.0) -> float:
    """Calculate Sharpe Ratio."""
    excess_returns = [r - risk_free_rate for r in returns]
    return np.mean(excess_returns) / np.std(excess_returns) if np.std(excess_returns) != 0 else 0

class OrderBook:
    """Simple order book implementation for high-frequency trading."""
    
    def __init__(self):
        self.bids = {}  # price -> quantity
        self.asks = {}  # price -> quantity
        self.last_update_time = 0
    
    def update(self, price: float, quantity: int, is_bid: bool) -> None:
        """Update the order book with a new order."""
        self.last_update_time = time.time()
        target = self.bids if is_bid else self.asks
        
        if quantity == 0:
            if price in target:
                del target[price]
        else:
            target[price] = quantity
    
    def get_best_bid(self) -> Tuple[float, int]:
        """Get best bid price and quantity."""
        if not self.bids:
            return 0, 0
        best_price = max(self.bids.keys())
        return best_price, self.bids[best_price]
    
    def get_best_ask(self) -> Tuple[float, int]:
        """Get best ask price and quantity."""
        if not self.asks:
            return float('inf'), 0
        best_price = min(self.asks.keys())
        return best_price, self.asks[best_price]
    
    def get_mid_price(self) -> float:
        """Get mid price between best bid and best ask."""
        best_bid, _ = self.get_best_bid()
        best_ask, _ = self.get_best_ask()
        
        if best_bid == 0 or best_ask == float('inf'):
            return 0
        
        return (best_bid + best_ask) / 2
    
    def get_spread(self) -> float:
        """Get spread between best bid and best ask."""
        best_bid, _ = self.get_best_bid()
        best_ask, _ = self.get_best_ask()
        
        if best_bid == 0 or best_ask == float('inf'):
            return float('inf')
        
        return best_ask - best_bid

def calculate_market_impact(order_size: int, average_daily_volume: int, volatility: float) -> float:
    """Estimate market impact of a trade using square root law."""
    impact_factor = 0.1  # Typical value, can be adjusted
    return impact_factor * volatility * np.sqrt(order_size / average_daily_volume)

def optimal_execution_time(order_size: int, daily_volume: int, urgency: float) -> float:
    """Calculate optimal execution time for a large order."""
    # Higher urgency means faster execution despite higher impact
    base_time = np.sqrt(order_size / daily_volume) * 24  # Base time in hours
    return base_time / urgency

def latency_compensation(ping_ms: float) -> float:
    """Calculate compensation time for network latency."""
    # Simple model: add 50% buffer to observed ping
    return ping_ms * 1.5 / 1000  # Convert to seconds

def time_to_microseconds(dt: datetime) -> int:
    """Convert datetime to microseconds since epoch, useful for precise timing."""
    epoch = datetime(1970, 1, 1)
    delta = dt - epoch
    return int(delta.total_seconds() * 1000000)

def microseconds_to_time(us: int) -> datetime:
    """Convert microseconds since epoch to datetime."""
    return datetime(1970, 1, 1) + timedelta(microseconds=us)