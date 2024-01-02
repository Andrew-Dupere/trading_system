import oandapyV20

import oandapyV20.endpoints.instruments as instruments

from oandapyV20 import API
import pandas as pd
import oandapyV20
from oandapyV20 import API
import oandapyV20.endpoints.instruments as instruments


import secretsarc

accountID = secretsarc.accountID
access_token = secretsarc.access_token
api = API(access_token=access_token, environment="practice")

granularity = 'M15'

def get_eurusd_price():
    """Fetch the current price of EUR/USD."""
    params = {
        "count": 1,
        "granularity": granularity
    }
    r = instruments.InstrumentsCandles(instrument="EUR_USD", params=params)
    api.request(r)
    latest_candle = r.response['candles'][-1]
    return float(latest_candle['mid']['c'])

# print(get_eurusd_price())

def calculate_stochastic_pandas(k_period=14, d_period=3):
    """
    Calculate Stochastic Oscillator using pandas.
    
    :param df: DataFrame with 'High', 'Low', 'Close' columns.
    :param k_period: Period for %K line calculation.
    :param d_period: Period for %D line calculation.
    :return: DataFrame with %K and %D.
    """
    params = {"count": 100, "granularity": granularity}  # M5 for 5-minute candles
    r = instruments.InstrumentsCandles(instrument="EUR_USD", params=params)
    api.request(r)
    data = r.response['candles']

    # Prepare DataFrame
    df = pd.DataFrame([{
        'High': float(candle['mid']['h']),
        'Low': float(candle['mid']['l']),
        'Close': float(candle['mid']['c'])
    } for candle in data])

    # Calculate %K
    low_min = df['Low'].rolling(window=k_period).min()
    high_max = df['High'].rolling(window=k_period).max()
    df['%K'] = 100 * ((df['Close'] - low_min) / (high_max - low_min))

    # Calculate %D
    df['%D'] = df['%K'].rolling(window=d_period).mean()

    return df[['%K', '%D']]

def calculate_moving_average(period, granularity=granularity):
    """
    Calculate the moving average for a given period.
    
    :param period: The period for the moving average.
    :param granularity: The granularity of the candles. Defaults to "M5".
    :return: The moving average value.
    """
    params = {"count": period, "granularity": granularity}
    r = instruments.InstrumentsCandles(instrument="EUR_USD", params=params)
    api.request(r)
    data = r.response['candles']

    # Prepare DataFrame
    df = pd.DataFrame([{
        'Close': float(candle['mid']['c'])
    } for candle in data])

    # Calculate Moving Average
    return df['Close'].rolling(window=period).mean().iloc[-1]

# Example usage
# ma_20 = calculate_moving_average(20)
# ma_50 = calculate_moving_average(50)

def determine_trend():
    # Calculate Moving Averages and Stochastic Indicator
    ma_fast = calculate_moving_average(8, "M15")
    ma_slow = calculate_moving_average(25, "M15")
    stochastic = calculate_stochastic_pandas(14, 3).iloc[-1]

    # Determine Trend
    if ma_fast > ma_slow and stochastic['%K'] > 70:
        # Uptre
        print("Uptrend detected - consider buying EUR/USD")
        return('b')
    elif ma_fast < ma_slow and stochastic['%K'] < 30:
        # Downtrend
        print("Downtrend detected - consider shorting EUR/USD")
        return('s')
    else:        
        print("No clear trend detected")
        return('n')

# Example usage

#print(determine_trend())   
