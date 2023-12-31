import account
import data

import secretsarc

balance = account.account_value
instrument = "EUR_USD"

#closes a position if it has lost more than 2% or gained more tahn 5% of the account balanace
account.close_position_if_necessary

#returns a buy or sell signal by checking moving average and stochastic indicators 
trend = data.determine_trend()

#creates a buy or sell order based on trend indicators and sizes the postion based on account balance
account.create_order(instrument=instrument, balance=balance, trend=trend)





