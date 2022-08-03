import numpy as np
import os
import pandas as pd
from datetime import datetime, timedelta

class Walk(object):
  def __init__(self, data: pd.DataFrame, 
               deathCrosses: [], 
               changePoints: []):
    self._data = data
    self._deathCrosses = deathCrosses 
    self._changePoints = changePoints
    self._partByCross = []
    self._partByChangePoint = []
    self._statsForChangePoint = []
    for cross in deathCrosses:
      p = self._data.loc[cross[0]:cross[1]]
      self._partByCross.append(p)
    for i in range(0, len(changePoints)-1):
      p = self._data.loc[changePoints[i]:changePoints[i + 1]] 
      self._partByChangePoint.append(p)
      self._statsForChangePoint.append(p["Close"].describe())

  def walk(self) -> pd.DataFrame:
# Walk thru each date in the data set
    dates = []
    price = []
    shouldDCAFor25th = []
    shouldDCAFor50th = []
    inBearMarket = []
    for index, row in self._data.iterrows():    
# Determine what change point partition the date belongs to
      shouldDCA = False
      i = 0
      for p in self._partByChangePoint:
        if index in p.index:
          if row["Close"] <= self._statsForChangePoint[i].loc["25%"]:
            dates.append(index)
            price.append(row["Close"])
            shouldDCAFor25th.append(True)
            shouldDCAFor50th.append(False)
            shouldDCA = True
          elif row["Close"] <= self._statsForChangePoint[i].loc["50%"]:
            dates.append(index)
            price.append(row["Close"])
            shouldDCAFor25th.append(False)
            shouldDCAFor50th.append(True)
            shouldDCA = True
          break
        i += 1
# Identify the dates occurring in a Bear market
      if shouldDCA:
        tagBear = False
        for p in self._partByCross:      
          if index in p.index:
            inBearMarket.append(True)
            tagBear = True
            break
        if not tagBear:
          inBearMarket.append(False)

    dfWalk = pd.DataFrame({}) 
    dfWalk["Date"] = dates
    dfWalk["Price"] = price
    dfWalk["ShouldDCAFor25th"] = shouldDCAFor25th
    dfWalk["ShouldDCAFor50th"] = shouldDCAFor50th
    dfWalk["inBearMarket"] = inBearMarket

    return dfWalk 
