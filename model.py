import changepoint as cp
import json
import numpy as np
import os
import pandas as pd
import ruptures as rpt
import sma
from datetime import datetime, timedelta
from walk import Walk

class Model(object): 
  def __init__(self, w: Walk):
    self._df = w.walk()
    if len(self._df) == 0:
      raise Exception("Walk didn't identify candidate purchases")

  def backtest(self, p: []) -> str:
    lastPrice = self._df.loc[len(self._df) - 1]["Price"]
    quantity = 0.0
    cost = 0.0
    for index, row in self._df.iterrows(): 
      if row["ShouldDCAFor25th"]:
        if row["inBearMarket"]:
          quantity += (p["Percentile25"] / row["Price"]) * p["BearMultiplier"]
          cost += p["Percentile25"] * p["BearMultiplier"]
        else:
          quantity += p["Percentile25"] / row["Price"] 
          cost += p["Percentile25"]
      else:
        if row["inBearMarket"]:
          quantity += (p["Percentile50"] / row["Price"]) * p["BearMultiplier"]
          cost += p["Percentile50"] * p["BearMultiplier"]
        else:
          quantity += p["Percentile50"] / row["Price"] 
          cost += p["Percentile50"]
    
    result = {}
    result["Data"] = p["Data"] 
    result["StartDate"] = p["StartDate"]
    result["EndDate"] = p["EndDate"]
    result["Percentile25"] = p["Percentile25"]
    result["Percentile50"] = p["Percentile50"]
    result["BearMultiplier"] = p["BearMultiplier"]
    result["Quantity"] = quantity 
    result["Cost"] = cost
    result["Value"] = lastPrice * quantity
    result["Profit"] = lastPrice * quantity - cost
    return json.dumps(result)

def backtest(p):
# Read configuration input 
  cfgData = p["Data"]
  cfgStartDate = p["StartDate"]
  cfgEndDate = p["EndDate"]

# Only extract Date and Closing Price
  df = pd.read_csv(cfgData)
  df = df[["Date", "Close"]]
  df["Date"] = pd.to_datetime(df["Date"], format="%Y-%m-%d")
  df.index = df.pop("Date")   

# Add SMA for 50 days
  dfSMA50 = sma.aggregateDfWithSMA(df, cfgStartDate, cfgEndDate, n=50)
  dfSMA50.index = dfSMA50.pop("Date")   

# Add SMA for 200 days
  dfSMA200 = sma.aggregateDfWithSMA(df, cfgStartDate, cfgEndDate, n=200)
  dfSMA200.index = dfSMA200.pop("Date")   

# Get Death Crosses
  crosses, dfCrosses = sma.getDeathCrosses(dfSMA50, dfSMA200)
      
# Get Change Point Dates
  dfClose = np.array(df.loc[cfgStartDate:cfgEndDate]["Close"])
  changePoints = cp.detectChangePoint(dfClose)
  dates = cp.getChangePointDates(dfCrosses, changePoints)

# Walk and back test
  try:
    w = Walk(df, crosses, dates)
    m = Model(w)
    result = m.backtest(p)
  except Exception:
    result = "Model does not suggest any purchases between {0} and {1}".format(p["StartDate"], p["EndDate"])
     
  return result 
