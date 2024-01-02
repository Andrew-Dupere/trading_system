This is a currency trading bot using the Oanda Broker. 

The account.py and data.py file pull information and execute trades. 

The api and frontend directories contain a webapp to display a dashboard of trade info.

The main.py file runs as a cron job every 5 minutes to operate the trading bot.

The algo starts by checking the account to see if any positions have lost more than 2% or gained more than 5% of the account balance and closes those positions.
Then the trend signal is determined using the 8 and 23 moving averages and the stochastic indicator, which are calculated in the data.py file.
Orders are then created based on trend signals and successfull orders are saved to the trade_log database. If no database file exists then one will be created.   
