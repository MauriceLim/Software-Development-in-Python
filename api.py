# api.py
from typing import Optional
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from datetime import datetime, timedelta
import yfinance as yf
from bs import MyBlackScholes  

app = FastAPI()

class MyBlackScholesResponse(BaseModel):
    stock_symbol: str  
    is_call_option: bool  
    interest_rate: float  
    dividend_rate: float  
    volatility: float  
    time_to_expiry: float  
    observation_date: Optional[str]
    result: dict

def get_stock_price_new(stock_symbol: str, observation_date: str):
    ticker = yf.Ticker(stock_symbol)

    if ticker.history(period="1d").empty:
        raise HTTPException(status_code=404, detail="Stock symbol not found or Inconsistent Date")

    try:
        if observation_date is not None:
            start_date = datetime.strptime(observation_date, "%Y-%m-%d")
            end_date = start_date + timedelta(days=1)

            data = yf.download(
                stock_symbol,
                start=start_date.strftime("%Y-%m-%d"),
                end=end_date.strftime("%Y-%m-%d")
            )
        else:
            data = ticker.history(period='1d')

        if data.empty or 'Close' not in data.columns:
            raise HTTPException(status_code=404, detail="Stock symbol not found or Inconsistent Date")

        return data['Close'][0]

    except Exception as e:
        raise HTTPException(status_code=404, detail="Inconsistent Date")

@app.get("/hw5/my-black-scholes/{stock_symbol}", response_model=MyBlackScholesResponse)
def calculate_option_new(stock_symbol: str,
                     is_call_option: bool,
                     strike_price: float,  # Change the name of the variable
                     interest_rate: float,
                     dividend_rate: float,
                     volatility: float,
                     time_to_expiry: float,
                     observation_date: Optional[str] = None):
    # get the stock price
    stock_price = get_stock_price_new(stock_symbol, observation_date)

    # Create an instance of the MyBlackScholes class
    option = MyBlackScholes()

    # Call the appropriate methods from the MyBlackScholes class
    option_price_result = option.calculate_option_price(
        is_call=is_call_option,
        S=stock_price,
        K=strike_price,
        T=time_to_expiry,
        r=interest_rate,
        q=dividend_rate,
        sigma=volatility
    )

    # Modify this line to use the greeks method from the MyBlackScholes class
    greeks_result = option.calculate_greeks(
        is_call=is_call_option,
        S=stock_price,
        K=strike_price,
        T=time_to_expiry,
        r=interest_rate,
        q=dividend_rate,
        sigma=volatility
    )

    response = {
        "stock_symbol": stock_symbol,
        "is_call_option": is_call_option,
        "interest_rate": interest_rate,
        "dividend_rate": dividend_rate,
        "volatility": volatility,
        "time_to_expiry": time_to_expiry,
        "observation_date": observation_date,
        "result": {
            "option_price": option_price_result,
            "greeks": greeks_result
        }
    }

    return response

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=5000)
