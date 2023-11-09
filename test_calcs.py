import pytest
from bs import black_scholes_dividend  # Import the function to be tested
from bm import crr_binomial_option_pricing

def test_bs_call_option():
    S = 40  # Current stock price
    K = 40  # Strike price
    T = 0.5  # Time to expiration (in years)
    r = 0.09  # Risk-free interest rate
    sigma = 0.3  # Volatility
    q = 0.03  # Dividend yield
    option_type = 'call'

    # Expected call option price from Hull's example
    expected_price = 3.89

    # Calculate the call option price using the function
    calculated_price = black_scholes_dividend(option_type, S, K, T, r, sigma, q)

    # Assert that the calculated price matches the expected price
    assert pytest.approx(calculated_price, abs=1e-2) == expected_price


def test_bs_put_option():
    S = 40  # Current stock price
    K = 40  # Strike price
    T = 0.5  # Time to expiration (in years)
    r = 0.09  # Risk-free interest rate
    sigma = 0.3  # Volatility
    q = 0.03  # Dividend yield
    option_type = 'put'

    # Expected put option price from Hull's example
    expected_price = 2.73

    # Calculate the put option price using the function
    calculated_price = black_scholes_dividend(option_type, S, K, T, r, sigma, q)

    # Assert that the calculated price matches the expected price
    assert pytest.approx(calculated_price, abs=1e-2) == expected_price

def test_binomial_european_call():
    S = 810  # Current stock price
    K = 800  # Strike price
    T = 0.5  # Time to expiration (in years)
    r = 0.05  # Risk-free interest rate
    sigma = 0.2  # Volatility
    time_steps = 2
    q = 0.02  # Dividend yield
    option_type = 'call'

    # Expected call option price from Hull's example 13.1
    expected_price = 53.39

    # Calculate the call option price using the function
    calculated_price = crr_binomial_option_pricing(S, K, T, r, sigma, time_steps, option_type, q)
    # Assert that the calculated price matches the expected price
    assert pytest.approx(calculated_price, abs=1e-2) == expected_price


def test_binomial_american_put():
    S = 50  # Current stock price
    K = 52  # Strike price
    T = 2  # Time to expiration (in years)
    r = 0.05  # Risk-free interest rate
    sigma = 0.3  # Volatility
    time_steps = 2
    q = 0  # Dividend yield
    option_type = 'put'
    is_american = True

    # Expected put option price from Hull's example 13.9
    expected_price = 7.43

    # Calculate the call option price using the function
    calculated_price = crr_binomial_option_pricing(S, K, T, r, sigma, time_steps, option_type, q, is_american)
    # Assert that the calculated price matches the expected price
    assert pytest.approx(calculated_price, abs=1e-2) == expected_price