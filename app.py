import json
import model
import datetime
import seaborn as sns
import streamlit as st
from PIL import Image

image = Image.open("./images/cloudera-logo.png")
st.sidebar.image(image) 

st.header("Algorithmic Crypto Dollar Cost Averaging")
st.markdown(
    """    
    An algorithmic DCA approach walks through the data set of crypto prices using the mean and standard deviation 
    for each change point segment.If the daily price resides within the 50th percentile, a purchase is made. 
    If the daily price resides within the 25th percentile a bigger purchase made. If the time period resides within 
    a "Death Cross", the purchase amount is multiplied by a specified factor.The purpose of the above measures is to 
    spend more $ only when the price is perceived as being low.

    As an alternative, a naive Dollar Cost Averaging (DCA) approach suggests investing a fixed amount of $ on a 
    recurring basis regardless of the crypto price.
    """
)

assetMap = { 
             "BTC": "./data/BTC-USD.csv",
             "ETH": "./data/ETH-USD.csv"
           }

assetChoice = st.sidebar.selectbox("Crypto Asset", options=["BTC", "ETH"])
  
startDate = st.sidebar.date_input("Start Date", value = datetime.date(2018, 6, 10), 
                                   min_value = datetime.date(2017, 1, 1), 
                                   max_value = datetime.date(2022, 6, 10))

endDate = st.sidebar.date_input("End Date", value = datetime.date(2022, 6, 10), 
                                 min_value = datetime.date(2017, 1, 1), 
                                 max_value = datetime.date(2022, 6, 10))

percentile25 = st.sidebar.number_input("$ for 25th Percentile", value = 20.0, min_value = 0.0, step = 1.0)

percentile50 = st.sidebar.number_input("$ for 50th Percentile", value = 10.0, min_value = 0.0, step = 1.0)

bearMultiplier = st.sidebar.number_input("Bear Market Multiplier", value = 4.0, min_value = 1.0, step = 1.0)

modelChoice = st.sidebar.selectbox("Model", options=["Pruned Exact Linear Time"])

modelInput = {
  "Data": assetMap[assetChoice],
  "StartDate": str(startDate),
  "EndDate": str(endDate),
  "Percentile25": percentile25,
  "Percentile50": percentile50,
  "BearMultiplier": bearMultiplier,
  "Model": modelChoice
}

if (endDate - startDate) <= datetime.timedelta(days=90):
  st.json('{ "Error": "No. of days between end and start should be >= 90 days" }')
else:
  dResult = json.loads(model.backtest(modelInput))  
  dResult["Cost"] = "${:,.2f}".format(float(dResult["Cost"]))
  dResult["Value"] = "${:,.2f}".format(float(dResult["Value"]))
  dResult["Profit"] = "${:,.2f}".format(float(dResult["Profit"]))
  result = json.dumps(dResult)
  st.json(result)


