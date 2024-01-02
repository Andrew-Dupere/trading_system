import account
import data

import secretsarc




balance = account.account_value
instrument = "EUR_USD"

price = data.get_eurusd_price()

#closes a position if it has lost more than 2% or gained more tahn 5% of the account balanace
account.close_position_if_necessary
    
#returns a buy or sell signal by checking moving average and stochastic indicators 
trend = data.determine_trend()

#execute an order based on trend signal and log it to the database
account.create_order_and_log(instrument=instrument, balance=balance, trend=trend, price=price)



