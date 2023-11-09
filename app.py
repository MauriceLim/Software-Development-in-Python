import argparse
import bs
import mc
import bm

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("model", type=str, choices=['bs', 'mc', 'bm'], help="Black-Scholes, Monte-Carlo, or Binomial-Model")
    parser.add_argument("--american", action="store_true", help="Specify '--american' for American Option")
    parser.add_argument("type", type=str, choices=['call', 'put'], help="Option type: 'call' or 'put'")
    parser.add_argument("stock_price", type=float, help="Stock price")
    parser.add_argument("strike_price", type=float, help="Strike price")
    parser.add_argument("rf", type=float, help="Risk-free rate")
    parser.add_argument("sigma", type=float, help="Stock price volatility")
    parser.add_argument("T", type=float, help="Time to maturity for the option")
    parser.add_argument("q", type=float, default=0, help="Dividend yield")
    parser.add_argument("n_sim", default=10, type=int, help="Number of simulations for binomial model, and Monte Carlo")
    parser.add_argument("n_time_steps", default=1, type=int, help="Number of time steps for Monte Carlo")
    args = parser.parse_args()

    if args.stock_price < 0:
        print("Stock price must be strictly greater than 0")
        exit(1)
    
    if args.strike_price < 0:
        print("Strike price must be strictly greater than 0")
        exit(1)

    if args.rf < 0:
        print("Assume a positive rate")
        exit(1)

    if args.sigma < 0:
        print("Volatility must be strictly greater than 0")
        exit(1)
    
    if args.T <= 0:
        print("Time to maturity cannot be negative")
        exit(1)
    
    if args.q < 0:
        print("Dividend yield must be strictly greater than 0")
        exit(1)
    
    if args.n_sim < 1:
        print("Number of simulations must be an integer greater than 0")
        exit(1)
    
    if args.n_time_steps < 1:
        print("Number of time steps must be an integer greater than 0")
        exit(1)
    
    if args.model == 'bs':
        if args.american:
            print("Only European options supported in Black-Scholes")
            exit(1)
        else: 
            bs1 = bs.black_scholes_dividend(args.type, args.stock_price, args.strike_price, args.T, args.rf, args.sigma, args.q)
            print(bs1)

    elif args.model == 'mc':
        if args.american:
            print("Only European options supported in Monte Carlo")
            exit(1)
        else:
            mc1 = mc.monte_carlo_option_pricing_antithetic(args.type, args.stock_price, args.strike_price, args.T, args.rf, args.sigma, args.q, args.n_sim, args.n_time_steps)
            print(mc1)

    else: 
        if args.american:
            bm2 = bm.crr_binomial_option_pricing(args.stock_price, args.strike_price, args.T, args.rf, args.sigma, args.n_sim, args.type, args.q, True)
            print(bm2)
        else:
            bm1 = bm.crr_binomial_option_pricing(args.stock_price, args.strike_price, args.T, args.rf, args.sigma, args.n_sim, args.type, args.q, False)
            print(bm1)
