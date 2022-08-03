import numpy as np
import pandas as pd
import ruptures as rpt
from datetime import datetime

def detectChangePoint(val: np.array) -> np.array:
  algo = rpt.Pelt(model="rbf").fit(val)
  result = algo.predict(pen=10)
  return result

def getChangePointDates(df: pd.DataFrame, 
                        checkpoints: []) -> [datetime]:
  chk = checkpoints[:-1]
  dates = [ df.index[i] for i in chk ]
  dates.append(df.index[len(df) - 1])
  return dates
