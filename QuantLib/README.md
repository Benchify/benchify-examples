# QuantLib - High-Speed Trading Utilities

This library provides essential quantitative finance utilities optimized for high-frequency and algorithmic trading applications.

## Features

- Price calculations: VWAP, TWAP, EMA, SMA
- Technical indicators: Bollinger Bands, RSI, MACD
- Order book management
- Market impact estimation
- Execution optimization
- Latency compensation
- High-precision timing utilities
- Performance metrics (Sharpe ratio)

## Usage

Import the needed functions from `trading_utils.py`:

```python
from trading_utils import calculate_vwap, OrderBook, calculate_bollinger_bands

# Example: Calculate VWAP
prices = [100.5, 100.7, 100.8, 101.2, 101.0]
volumes = [500, 350, 750, 800, 600]
vwap = calculate_vwap(prices, volumes)

# Example: Use order book
book = OrderBook()
book.update(100.5, 500, True)  # Add bid
book.update(100.8, 300, False)  # Add ask
mid_price = book.get_mid_price()
```

The library is designed for performance and efficiency in high-speed trading environments.