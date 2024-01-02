import os
import sqlite3
from flask import Flask, jsonify

app = Flask(__name__)

# Get the directory of the script
script_directory = os.path.dirname(os.path.abspath(__file__))
parent_directory = os.path.dirname(script_directory)

# Create the full path for the database file
database_path = os.path.join(parent_directory, 'trade_log.db')

def get_last_20_trades():
    try:
        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()
        
        # Query the last 20 trades from the 'trades' table
        cursor.execute('''
            SELECT * FROM trades
            ORDER BY timestamp DESC
            LIMIT 20
        ''')
        
        trades = cursor.fetchall()
        conn.close()
        
        return trades
    except sqlite3.Error as e:
        print(f"Error querying the database: {e}")
        return []

@app.route('/api/last_20_trades', methods=['GET'])
def last_20_trades():
    trades = get_last_20_trades()
    return jsonify(trades)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
