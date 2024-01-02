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


import sqlite3
import os 

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

# Get the directory of the script
script_directory = os.path.dirname(os.path.abspath(__file__))

# Create the full path for the database file
database_path = os.path.join(script_directory, 'trade_log.db')

def create_trade_database():
    try:
        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()
        
        # Create a table to store trade details if it doesn't exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS trades (
                timestamp TEXT,
                instrument TEXT,
                price REAL,
                order_type TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
        print(f"Database '{database_path}' and table 'trades' created or already exists.")
    except sqlite3.Error as e:
        print(f"Error creating the database: {e}")

def create_order_and_log(instrument, balance, trend, price):
    """
    Create a market order for the specified instrument based on account balance and trend.
    Log the trade details to the database.
    
    Args:
        instrument (str): The trading instrument (e.g., 'EUR_USD').
        balance (float): The account balance.
        trend (str): The trading trend ('b' for buy, 's' for sell).
        price (float): The price of the EUR/USD at the time of the trade.
    """
    if trend not in ['b', 's']:
        print("No action taken.")
        return 'n'

    # Calculate position size as 10% of the account balance
    position_size = 0.10 * balance

    # Determine order units based on trend
    if trend == 'b':
        units = int(position_size)
        order_type = 'buy'
    else:
        units = -int(position_size)
        order_type = 'sell'

    # Create a market order request
    mkt_order = MarketOrderRequest(instrument=instrument, units=units)

    # Submit the order request
    r = orders.OrderCreate(accountID=accountID, data=mkt_order.data)
    api.request(r)

    # Check if the database file exists, and create it if not
    if not os.path.isfile(database_path):
        create_trade_database()

    # Check if the 'trades' table exists, and create it if not
    try:
        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM trades LIMIT 1")  # Try to select from the table
    except sqlite3.Error:
        # Table does not exist, create it
        cursor.execute('''
            CREATE TABLE trades (
                timestamp TEXT,
                instrument TEXT,
                price REAL,
                order_type TEXT
            )
        ''')
        conn.commit()
    
    # Log trade details to the database
    try:
        cursor.execute('''
            INSERT INTO trades (timestamp, instrument, price, order_type)
            VALUES (datetime('now'), ?, ?, ?)
        ''', (instrument, price, order_type))
        conn.commit()
        conn.close()
        print("Trade logged successfully.")
    except sqlite3.Error as e:
        print(f"Error logging the trade: {e}")

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


