import numpy as np
from scipy.stats import norm

class BlackScholes:
    @staticmethod
    def calculate_option_price(is_call, S, K, T, r, q, sigma):
        d1 = (np.log(S / K) + (r - q + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
        d2 = d1 - sigma * np.sqrt(T)

        if is_call:
            option_price = S * np.exp(-q * T) * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
        else:
            option_price = K * np.exp(-r * T) * norm.cdf(-d2) - S * np.exp(-q * T) * norm.cdf(-d1)

        return option_price

    @staticmethod
    def calculate_greeks(is_call, S, K, T, r, q, sigma):
        d1 = (np.log(S / K) + (r - q + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
        d2 = d1 - sigma * np.sqrt(T)

        if is_call:
            delta = np.exp(-q * T) * norm.cdf(d1)
            gamma = np.exp(-q * T) * norm.pdf(d1) / (S * sigma * np.sqrt(T))
        else:
            delta = -np.exp(-q * T) * norm.cdf(-d1)
            gamma = np.exp(-q * T) * norm.pdf(d1) / (S * sigma * np.sqrt(T))

        theta = -((S * sigma * np.exp(-q * T) * norm.pdf(d1)) / (2 * np.sqrt(T))) - r * K * np.exp(-r * T) * norm.cdf(d2)
        vega = S * np.exp(-q * T) * np.sqrt(T) * norm.pdf(d1)
        rho = K * T * np.exp(-r * T) * norm.cdf(d2)

        return {
            'delta': delta,
            'gamma': gamma,
            'theta': theta,
            'vega': vega,
            'rho': rho
        }
