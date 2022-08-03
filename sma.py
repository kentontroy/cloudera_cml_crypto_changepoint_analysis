import numpy as np
import pandas as pd
from datetime import datetime, timedelta

def aggregateDfWithSMA(df: pd.DataFrame, 
                       begin: str, 
                       end: str, 
                       n: int) -> pd.DataFrame:
  firstDate = datetime.strptime(begin, "%Y-%m-%d")
  lastDate  = datetime.strptime(end, "%Y-%m-%d")
  targetDate = firstDate
  dates = []
  X, Y = [], []
  lastTime = False
  while True:
    dfOffset = df.loc[:targetDate].tail(n + 1)
    if len(dfOffset) != n + 1:
      print(f"Error: Window of size {n} is too large for date {targetDate}")
      return
    values = dfOffset.to_numpy()
    x, y = values[:-1], values[-1]
    dates.append(targetDate)
    X.append(np.mean(x))
    Y.append(y)

    nextWeek = df.loc[targetDate:targetDate + timedelta(days=7)]
    nextDatetime = str(nextWeek.head(2).tail(1).index.values[0])
    year, month, day = nextDatetime.split("T")[0].split("-")
    nextDate = datetime(day=int(day), month=int(month), year=int(year))
    targetDate = nextDate
    if lastTime:
      break
    if targetDate == lastDate:
      lastTime = True
    
  dfWindowed = pd.DataFrame({})
  dfWindowed["Date"] = dates
  dfWindowed["Close"] = Y
  dfWindowed[f"SMA-{n}"] = X

  return dfWindowed

def getDeathCrosses(dfSMA50: pd.DataFrame, 
                    dfSMA200: pd.DataFrame) -> ([], pd.DataFrame):
# Join the two data sets
  dfMerged = pd.merge(dfSMA50, dfSMA200, on="Date")
  dfMerged.drop(["Close_y"], axis=1, inplace=True)
  dfMerged.rename(columns={"Close_x": "Close"}, inplace=True)

  dfDeathCross = dfMerged[(dfMerged["SMA-50"] < dfMerged["SMA-200"])]
  dfGoldenCross = dfMerged[(dfMerged["SMA-50"] > dfMerged["SMA-200"])]
  dfCrosses = pd.merge(dfDeathCross, dfGoldenCross, 
                       how="outer", suffixes=("_death", "_golden"),
                       on="Date")
  dfCrosses.sort_index(ascending=True, inplace=True)
# Get Death Crosses by start date, max price % drop, and duration
  crosses = []
  x = [] 
  t = []
  analytics = []
  startPrice = 0.0
  for index, row in dfCrosses.iterrows():
    if len(x) != 0 and np.isnan(row["Close_death"]):
      decline = (startPrice - np.min(x))/startPrice
      analytics.append((np.min(t), np.max(t), decline, (np.max(t)-np.min(t)).days))
      x.clear() 
      t.clear()
    elif np.isnan(row["Close_golden"]):
      if len(x) == 0:
        startPrice = row["Close_death"]
      x.append(row["Close_death"])
      t.append(index)
  for a in analytics:
    startDate, endDate, priceDrop, duration = a
    crosses.append((startDate, endDate, priceDrop[0], duration))
  return crosses, dfCrosses

