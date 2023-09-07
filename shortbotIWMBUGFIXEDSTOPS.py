shortbotIWMBUGFIXEDSTOPS.py
shortbotIWM.py 
import pandas as pd
import matplotlib.pyplot as plt
from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract

# Define Interactive Brokers client 
class IWMbot(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)
        self.data = []
        self.historical_data = None  
        self.order_id = None
        self.entry_price = None
        self.max_loss = 0.11  
        self.entry_threshold = 0.5
        self.short_ma = 10  
        self.long_ma = 30
        self.previous_short_ma = None
        self.previous_long_ma = None
        
    def historicalData(self, reqId, bar):
        ...  # Same as before
        
    def historicalDataEnd(self, reqId, start:str, end:str):
        ...  # Same as before
        
        # Check if a limit order should be placed
        if (some condition): 
            limit_price = ...
            self.placeLimitOrder(self.order_id, "BUY", 100, limit_price) 
            
        # Implement fix or kill order 
        if (15 seconds have passed and order not filled):
            self.cancelOrder(self.order_id)
            self.order_id = None  
            
        # Update stop loss 
        current_price = df["Close"][-1]
        loss = (self.entry_price - current_price) / self.entry_price
        if loss > self.max_loss:
            self.placeStopOrder(self.order_id, "SELL", 100, current_price)  
            
        # Recalibrate entry if order not filled after n seconds
        if (self.order_id is None and n seconds have passed):  
            self.historical_data = pd.DataFrame(self.historical_data, columns=['Date', 'Open', 'High', 'Low', 'Close', 'Volume'])
            ma20 = self.historical_data["Close"].rolling(20).mean()
            last_close = self.historical_data["Close"][-1]
            
            # Check if close is 0.5% above/below 20-day MA, if so enter the position
            if (last_close > 1.005 * ma20[-1] or last_close < 0.995 * ma20[-1]): 
                self.entry_price = last_close
                ...  # Place buy/sell order and save order_id
                
        # Check if we should enter a short position
        short_ma = self.historical_data["Close"][-self.short_ma:].mean()
        long_ma = self.historical_data["Close"][-self.long_ma:].mean()
        
        # Enter short if short-term MA crosses below long-term MA
        if (short_ma < long_ma and self.previous_short_ma > self.previous_long_ma):  
            self.entry_price = self.historical_data["Close"][-1]
            self.placeOrder("SELL", 100)  
            
        # Exit short if short-term MA crosses above long-term MA
        elif (short_ma > long_ma and self.previous_short_ma < self.previous_long_ma):  
            self.placeOrder("BUY", 100)  
            
        # Save previous MA values 
        self.previous_short_ma = short_ma
        self.previous_long_ma = long_ma
        
    ...  # Rest of the methods       

# Connect to IB API and run event loop
bot = IWMbot()
bot.connect("127.0.0.1", 7497, 0) 
bot.run()
bot.disconnect()


