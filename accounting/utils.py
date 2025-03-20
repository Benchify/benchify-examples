from typing import List, Tuple, Dict

# Function to calculate the internal rate of return (IRR) for a series of cash flows
# cash_flows: list of cash flows, including the initial investment as a negative number
def calculate_irr(cash_flows: List[float], guess: float = 0.1) -> float:
    """
    Calculate the internal rate of return (IRR) for a series of cash flows.

    :param cash_flows: List of cash flows, including the initial investment as a negative number
    :param guess: Initial guess for the IRR
    :return: Internal rate of return
    """
    max_iterations = 1000
    tolerance = 1e-6
    rate = guess

    for _ in range(max_iterations):
        npv = sum(cf / (1 + rate) ** i for i, cf in enumerate(cash_flows))
        derivative = sum(-i * cf / (1 + rate) ** (i + 1) for i, cf in enumerate(cash_flows))
        new_rate = rate - npv / derivative
        if abs(new_rate - rate) < tolerance:
            return new_rate
        rate = new_rate

    raise ValueError("IRR calculation did not converge")

# Function to calculate the net present value (NPV) of a series of cash flows
# cash_flows: list of cash flows, rate: discount rate
def calculate_npv(cash_flows: List[float], rate: float) -> float:
    """
    Calculate the net present value (NPV) of a series of cash flows.

    :param cash_flows: List of cash flows
    :param rate: Discount rate
    :return: Net present value
    """
    return sum(cf / (1 + rate) ** i for i, cf in enumerate(cash_flows))

# Function to calculate the modified internal rate of return (MIRR)
# cash_flows: list of cash flows, finance_rate: finance rate, reinvest_rate: reinvestment rate
def calculate_mirr(cash_flows: List[float], finance_rate: float, reinvest_rate: float) -> float:
    """
    Calculate the modified internal rate of return (MIRR) for a series of cash flows.

    :param cash_flows: List of cash flows
    :param finance_rate: Finance rate
    :param reinvest_rate: Reinvestment rate
    :return: Modified internal rate of return
    """
    positive_flows = sum(cf / (1 + reinvest_rate) ** i for i, cf in enumerate(cash_flows) if cf > 0)
    negative_flows = sum(cf / (1 + finance_rate) ** i for i, cf in enumerate(cash_flows) if cf < 0)
    n = len(cash_flows)
    return (positive_flows / abs(negative_flows)) ** (1 / (n - 1)) - 1

# Function to calculate the value at risk (VaR) for a portfolio
# portfolio_returns: list of portfolio returns, confidence_level: confidence level for VaR
def calculate_var(portfolio_returns: List[float], confidence_level: float) -> float:
    """
    Calculate the value at risk (VaR) for a portfolio.

    :param portfolio_returns: List of portfolio returns
    :param confidence_level: Confidence level for VaR (e.g., 0.95 for 95%)
    :return: Value at risk
    """
    sorted_returns = sorted(portfolio_returns)
    index = int((1 - confidence_level) * len(sorted_returns))
    return abs(sorted_returns[index])

# Function to calculate the expected shortfall (ES) for a portfolio
# portfolio_returns: list of portfolio returns, confidence_level: confidence level for ES
def calculate_es(portfolio_returns: List[float], confidence_level: float) -> float:
    """
    Calculate the expected shortfall (ES) for a portfolio.

    :param portfolio_returns: List of portfolio returns
    :param confidence_level: Confidence level for ES (e.g., 0.95 for 95%)
    :return: Expected shortfall
    """
    sorted_returns = sorted(portfolio_returns)
    index = int((1 - confidence_level) * len(sorted_returns))
    return abs(sum(sorted_returns[:index]) / index)

# Function to calculate the currency conversion given exchange rates
# amount: amount to convert, from_currency: currency code of the amount, to_currency: target currency code, exchange_rates: dictionary of exchange rates
def convert_currency(amount: float, from_currency: str, to_currency: str, exchange_rates: Dict[str, float]) -> float:
    """
    Convert an amount from one currency to another using given exchange rates.

    :param amount: Amount to convert
    :param from_currency: Currency code of the amount
    :param to_currency: Target currency code
    :param exchange_rates: Dictionary of exchange rates
    :return: Converted amount in the target currency
    """
    if from_currency == to_currency:
        return amount
    rate = exchange_rates[to_currency] / exchange_rates[from_currency]
    return amount * rate

# Function to calculate the compound annual growth rate (CAGR)
# initial_value: initial investment value, final_value: final investment value, periods: number of periods
def calculate_cagr(initial_value: float, final_value: float, periods: int) -> float:
    """
    Calculate the compound annual growth rate (CAGR).

    :param initial_value: Initial investment value
    :param final_value: Final investment value
    :param periods: Number of periods
    :return: Compound annual growth rate
    """
    return (final_value / initial_value) ** (1 / periods) - 1

# Function to calculate the Sharpe ratio for a portfolio
# portfolio_returns: list of portfolio returns, risk_free_rate: risk-free rate of return
def calculate_sharpe_ratio(portfolio_returns: List[float], risk_free_rate: float) -> float:
    """
    Calculate the Sharpe ratio for a portfolio.

    :param portfolio_returns: List of portfolio returns
    :param risk_free_rate: Risk-free rate of return
    :return: Sharpe ratio
    """
    excess_returns = [r - risk_free_rate for r in portfolio_returns]
    mean_excess_return = sum(excess_returns) / len(excess_returns)
    std_dev = (sum((r - mean_excess_return) ** 2 for r in excess_returns) / len(excess_returns)) ** 0.5
    return mean_excess_return / std_dev

# Function to calculate the beta of a stock
# stock_returns: list of stock returns, market_returns: list of market returns
def calculate_beta(stock_returns: List[float], market_returns: List[float]) -> float:
    """
    Calculate the beta of a stock.

    :param stock_returns: List of stock returns
    :param market_returns: List of market returns
    :return: Beta of the stock
    """
    covariance = sum((sr - sum(stock_returns) / len(stock_returns)) * (mr - sum(market_returns) / len(market_returns)) for sr, mr in zip(stock_returns, market_returns)) / len(stock_returns)
    market_variance = sum((mr - sum(market_returns) / len(market_returns)) ** 2 for mr in market_returns) / len(market_returns)
    return covariance / market_variance


