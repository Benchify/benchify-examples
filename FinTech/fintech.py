import numpy as np
import pandas as pd
from scipy import stats

def calculate_sharpe_ratio(returns, risk_free_rate=0.0):
    """
    Calculate the Sharpe ratio of a returns series.
    
    Args:
        returns (array-like): Daily or periodic returns of the portfolio
        risk_free_rate (float): Risk-free rate expressed in the same periodicity as returns
        
    Returns:
        float: Sharpe ratio
    """
    excess_returns = returns - risk_free_rate
    return np.mean(excess_returns) / np.std(excess_returns, ddof=1) * np.sqrt(252)  # Annualized for daily returns

def calculate_moving_average(prices, window):
    """
    Calculate the moving average of a price series.
    
    Args:
        prices (array-like): Series of prices
        window (int): Window size for the moving average
        
    Returns:
        array-like: Moving average series
    """
    return pd.Series(prices).rolling(window=window).mean().values

def calculate_bollinger_bands(prices, window=20, num_std=2):
    """
    Calculate Bollinger Bands for a price series.
    
    Args:
        prices (array-like): Series of prices
        window (int): Window size for the moving average
        num_std (int): Number of standard deviations to use
        
    Returns:
        tuple: (middle band, upper band, lower band)
    """
    prices_series = pd.Series(prices)
    middle_band = prices_series.rolling(window=window).mean()
    std = prices_series.rolling(window=window).std()
    
    upper_band = middle_band + (std * num_std)
    lower_band = middle_band - (std * num_std)
    
    return middle_band.values, upper_band.values, lower_band.values

def calculate_rsi(prices, window=14):
    """
    Calculate the Relative Strength Index (RSI) for a price series.
    
    Args:
        prices (array-like): Series of prices
        window (int): Window size for RSI calculation
        
    Returns:
        array-like: RSI values
    """
    delta = pd.Series(prices).diff().dropna()
    gains = delta.where(delta > 0, 0)
    losses = -delta.where(delta < 0, 0)
    
    avg_gain = gains.rolling(window=window).mean()
    avg_loss = losses.rolling(window=window).mean()
    
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    
    return rsi.values

def calculate_vwap(prices, volumes):
    """
    Calculate Volume-Weighted Average Price (VWAP).
    
    Args:
        prices (array-like): Series of prices
        volumes (array-like): Series of volumes corresponding to the prices
        
    Returns:
        array-like: VWAP values
    """
    prices = np.array(prices)
    volumes = np.array(volumes)
    
    cumulative_pv = np.cumsum(prices * volumes)
    cumulative_volume = np.cumsum(volumes)
    
    return cumulative_pv / cumulative_volume