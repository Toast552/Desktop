ShortbotTrailingStop.py
import pandas as pd
import matplotlib.pyplot as plt
from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract

# Define Interactive Brokers client 
class IWMbot(EClient, EWrapper):
    def __init__(self):
        ...
        self.short_ma = 10  # Short-term moving average
        self.long_ma = 30  # Long-term moving average
        
    def historicalData(self, reqId, bar):
        ...  # Same as before
        
    def historicalDataEnd(self, reqId, start:str, end:str):
        ...  # Same as before
        
        # Check if we should enter a short position
        self.historical_data = pd.DataFrame(self.historical_data, columns=['Date', 'Open', 'High', 'Low', 'Close', 'Volume'])
        short_ma = self.historical_data["Close"][-self.short_ma:].mean()
        long_ma = self.historical_data["Close"][-self.long_ma:].mean()
        
        # Enter short if short-term MA crosses below long-term MA
        if (short_ma < long_ma and self.previous_short_ma > self.previous_long_ma):  
            self.entry_price = self.historical_data["Close"][-1]
            self.placeOrder("SELL", 100)  # Place sell short order
            
        # Exit short if short-term MA crosses above long-term MA
        elif (short_ma > long_ma and self.previous_short_ma < self.previous_long_ma):  
            self.placeOrder("BUY", 100)  # Place buy to cover order
            
        # Save previous MA values 
        self.previous_short_ma = short_ma
        self.previous_long_ma = long_ma
        
    ...  # Rest of the methods       

# Connect to IB API and run event loop
bot = IWMbot()
bot.connect("127.0.0.1", 7497, 0)

# Fetch 30 days of 1 min data for IWM 
contract = Contract()
contract.symbol = "IWM"
contract.sec
