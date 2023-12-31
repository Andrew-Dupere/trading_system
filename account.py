import oandapyV20
import oandapyV20.endpoints.positions as positions

import oandapyV20.endpoints.orders as orders
import oandapyV20.endpoints.trades as trades
from oandapyV20 import API
from oandapyV20.contrib.requests import MarketOrderRequest

import oandapyV20.endpoints.accounts as accounts

import oandapyV20
from oandapyV20 import API
import oandapyV20.endpoints.instruments as instruments


import secretsarc

accountID = secretsarc.accountID
access_token = secretsarc.access_token
api = API(access_token=access_token, environment="practice")

account_details = accounts.AccountDetails(accountID)
api.request(account_details)
account_value = float(account_details.response['account']['balance'])


def fetch_open_positions():
    r = positions.OpenPositions(accountID=accountID)
    api.request(r)
    
    return r.response['positions']

fetch_open_positions()

def close_position_if_necessary(api=api, account_id=accountID):
    # Fetch current account details
    account_details = accounts.AccountDetails(account_id)
    api.request(account_details)
    account_value = float(account_details.response['account']['balance'])

    # Fetch open positions
    open_positions = positions.OpenPositions(account_id)
    api.request(open_positions)

    for position in open_positions.response['positions']:
        # Handle both long and short positions
        for side in ['long', 'short']:
            if position[side]['units'] != '0':  # Check if the position is open
                pl = float(position[side]['unrealizedPL'])
                loss_percentage = (pl / account_value) * 100

                # Close position if loss is more than 2%
                if loss_percentage >= -1:
                    for trade_id in position[side]['tradeIDs']:
                        r = trades.TradeClose(account_id, tradeID=trade_id)
                        api.request(r)

def create_order(instrument, balance, trend):
    """
    Create a market order for the specified instrument based on account balance and trend.
    
    Args:
        instrument (str): The trading instrument (e.g., 'EUR_USD').
        balance (float): The account balance.
        trend (str): The trading trend ('b' for buy, 's' for sell).
    """
    if trend not in ['b', 's']:
        print("no action taken")
        pass
        

    # Calculate position size as 10% of the account balance
    position_size = 0.10 * balance

    # Determine order units based on trend
    if trend == 'b':
        units = int(position_size)
    else:
        units = -int(position_size)

    # Create a market order request
    mkt_order = MarketOrderRequest(instrument=instrument, units=units)

    # Submit the order request
    r = orders.OrderCreate(accountID=accountID, data=mkt_order.data)
    api.request(r)

# Example usage:
# Assuming account_balance is the account balance, and trend is 'b' for buy or 's' for sell.
# create_order('EUR_USD', account_balance, trend)

    

# close_position_if_necessary()
# create_order("EUR_USD",10)
# print(len(fetch_open_positions()[0]['long']['tradeIDs']))
    


account_details = accounts.AccountDetails(accountID)
api.request(account_details)


# Fetch open positions
open_positions = api.request(positions.OpenPositions(accountID=accountID))
#api.request(open_positions)


#create order, fetch account info and close position functions working properly

# close_position_if_necessary()
# print(fetch_open_positions())

# x = fetch_open_positions
# close_position_if_necessary()
# y = fetch_open_positions
# print(x == y)

