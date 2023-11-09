import numpy as np

def monte_carlo_option_pricing_basic(option_type, S, K, T, r, sigma, q, n_simulations, n_time_steps):

    dt = T / n_time_steps
    simulation_results = np.zeros(n_simulations)

    for i in range(n_simulations):
        S_t = S
        for _ in range(n_time_steps):
            Z = np.random.standard_normal()
            S_t *= np.exp((r - q - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * Z)
        if option_type == 'call':
            option_payoff = max(0, S_t - K)
        elif option_type == 'put':
            option_payoff = max(0, K - S_t)
        else:
            raise ValueError("Invalid option type. Use 'call' or 'put'.")
        simulation_results[i] = option_payoff

    option_price = np.exp(-r * T) * np.mean(simulation_results)

    variance_of_estimator = np.exp(-2 * r * T) * np.var(simulation_results) / n_simulations
    
    return option_price, np.sqrt(variance_of_estimator)


def monte_carlo_option_pricing_antithetic(option_type, S, K, T, r, sigma, q, n_simulations, n_time_steps):

    dt = T / n_time_steps
    n_simulations_half = n_simulations // 2
    option_payoffs1 = np.zeros(n_simulations_half)
    option_payoffs2 = np.zeros(n_simulations_half)
    
    for i in range(n_simulations_half):
        Z1 = np.random.standard_normal(n_time_steps)
        Z2 = -Z1  # Generate the antithetic variate
        S_t1 = S * np.exp(np.cumsum((r - q - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * Z1))
        S_t2 = S * np.exp(np.cumsum((r - q - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * Z2))

        if option_type == 'call':
            option_payoffs1[i] = max(0, S_t1[-1] - K)
            option_payoffs2[i] = max(0, S_t2[-1] - K)
        elif option_type == 'put':
            option_payoffs1[i] = max(0, K - S_t1[-1])
            option_payoffs2[i] = max(0, K - S_t2[-1])

    option_price = np.exp(-r * T) * (np.mean(option_payoffs1) + np.mean(option_payoffs2)) / 2
    variance_of_estimator = np.exp(-2 * r * T) * np.var((option_payoffs1 + option_payoffs2)/2) / n_simulations
    
    return option_price, np.sqrt(variance_of_estimator)