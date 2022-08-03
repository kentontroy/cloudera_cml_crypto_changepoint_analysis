import cdsw
import json
import numpy as np
import os
import pandas as pd
import sys
from datetime import datetime, timedelta

@cdsw.model_metrics
def naivetest(param: str):
  cdsw.track_metric("input", param)
# Read configuration input 
  p = json.loads(param)
  cfgData = p["Data"]
  cfgStartDate = p["StartDate"]
  cfgEndDate = p["EndDate"]
  cfgDaysRecurring = p["DaysRecurring"]
  cfgFixedAmount = p["FixedAmount"]
    
# Only extract Date and Closing Price
  df = pd.read_csv(cfgData)
  df = df[["Date", "Close"]]
  df["Date"] = pd.to_datetime(df["Date"], format="%Y-%m-%d")
  df.index = df.pop("Date")   
  firstDate = datetime.strptime(cfgStartDate, "%Y-%m-%d")
  lastDate  = datetime.strptime(cfgEndDate, "%Y-%m-%d")
  df = df.loc[firstDate:lastDate]

# Walk and apply DCA
  nextDate = df.index[0]
  lastDate = df.index[len(df) - 1]
  lastPrice = df.loc[lastDate]["Close"]
  quantity = 0.0
  cost = 0.0
  fixedAmount = int(cfgFixedAmount)
  daysRecurring = int(cfgDaysRecurring)
  while True:
    quantity += fixedAmount / df.loc[nextDate]["Close"]
    cost += fixedAmount
    nextDate = nextDate + timedelta(days=daysRecurring)
    if nextDate > lastDate:
      break    

  result = {}
  result["Data"] = p["Data"]
  result["StartDate"] = p["StartDate"]
  result["EndDate"] = p["EndDate"]
  result["DaysRecurring"] = p["DaysRecurring"]
  result["FixedAmount"] = p["FixedAmount"]
  result["Quantity"] = quantity 
  result["Cost"] = cost
  result["Value"] = lastPrice * quantity
  result["Profit"] = lastPrice * quantity - cost
  results = json.dumps(result)

  cdsw.track_metric("naivetest_result", results)
  return results   

def main():
  args = sys.argv[1:]
  print(args[0])
  naivetest(args[0])

if __name__ == "__main__":
  main()

