import numpy as np

def crr_binomial_option_pricing(S, K, T, r, sigma, n, option_type, dividend_rate=0, is_american=False):
    dt = T / n
    u = np.exp(sigma * np.sqrt(dt))
    d = 1 / u
    q = (np.exp((r - dividend_rate) * dt) - d) / (u - d)
    discount_factor = np.exp(-r * dt)

    stock_price = np.zeros((n + 1, n + 1))
    option_price = np.zeros((n + 1, n + 1))

    # Calculate stock prices at each node
    for j in range(n + 1):
        for i in range(j + 1):
            stock_price[i, j] = S * (u ** (j - i)) * (d ** i)

    # Calculate option prices at expiration
    for i in range(n + 1):
        if option_type == 'call':
            option_price[i, n] = max(0, stock_price[i, n] - K)
        elif option_type == 'put':
            option_price[i, n] = max(0, K - stock_price[i, n])

    # Calculate option prices at earlier time steps
    for j in range(n - 1, -1, -1):
        for i in range(j + 1):
            option_price[i, j] = (q * option_price[i, j + 1] + (1 - q) * option_price[i + 1, j + 1]) * discount_factor

            if is_american:
                # Check for early exercise for American options
                option_price[i, j] = max(option_price[i, j], stock_price[i, j] - K if option_type == 'call' else K - stock_price[i, j])

    return option_price[0, 0]
