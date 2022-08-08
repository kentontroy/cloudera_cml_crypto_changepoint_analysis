# HODL Crypto with Naive and Algorithmic DCA
## HODL = ("Hold On For Dear Life")
## DCA  = ("Dollar Cost Averaging")

Consider the two analytical features below:

1. A Pruned Exact Linear Time (PELT) model is a class of algorithms used to segment a time series
into change points. The time series data within each change point displays a set of statistical properties
different than the change points before and after.

2. One bearish indicator for market data is the "Death Cross". A death cross occurs when the 50-day Simple 
Moving Average (SMA) falls below the 200-day SMA.

What is illustrated in the demo:

This Cloudera ML environment exposes a workspace to test how much money can be made by purchasing crypto 
when you can ascertain that the price is low.Looking at the entire range of prices for a crypto asset as 
one monolithic block of time having the same distribution is flawed. 

Change Point Analysis with PELT can be used to divide a large block of time into individual segments where 
each segment has its own statistical properties.

This project walks through a crypto price data set, on a daily basis, in a back testing fashion using historical
data.

As it walks through the data it uses the mean and standard deviation for each change point segment. If the
daily price resides within the 50th percentile, a purchase is made. If the daily price resides within the 25th
percentile a bigger purchase made. If the time period resides within a "Death Cross", the purchase amount is
multiplied by a specified factor. The purpose of the above measures is to spend more $ only when the price is 
perceived as being low.

As an alternative, a naive Dollar Cost Averaging (DCA) approach suggests investing a fixed amount of $ on a 
recurring basis regardless of the crypto price.

Experiements:

Cloudera ML can be used to compare and contrast PELT/SMA versus DCA. Some surprising conclusions result.


## Files

Modify the default files to get started with your own project.

* `README.md` -- This project's readme in Markdown format.
* `0.install-requirements.sh` -- Install the dependencies from requirements.txt
* `1.analysis.ipynb` -- An example Jupyter Notebook for exploratory data analysis
* `2.backtest.py` -- Run the PELT model to detect change points for crypto price movements in back testing mode
* `3.naivetest.py` -- Run a naive Dollar Cost Averaging program to make crypto purchases with no inference
* `requirements.txt` -- Dependencies that need to be manually installed if you (mainly numpy, pandas, ruptures)
* `cdsw-build.sh` -- A custom build script used for models and experiments. This
will pip install our dependencies, primarily pandas, numpy, and ruptures for Change Point analysis
* `sma.py` --  A Python file with data engineering steps to extra Simple Moving Averages (50 and 200 day)as features
* `changepoint.py` -- A Python file performing Change Point analysis using Pruned Exact Linear Time (PELT)
* `walk.py` -- A Python file that walks date-by-date thru the crypto prices data set and infers whether or not a buy
decision should be made

## Instructions for Sessions
1. Click "Open Workbench".
2. Launch a new Python session.

## Instructions for Experiments and Models
1. Click "Open Workbench".
2. Run an experiment with either 2.backtest or 3.naivetest.py as the input script.
3. Deploy the model using the Change Point Analysis and Bear Market testing`. Specify backtest`as the input function.

## Streamlit Application spawned by CML

<img src="./images/cml_screenshot" alt=""/><br>

## Example input for PELT Experiment
```
{
  "ModelVersion": "./models/backtest-run-1axsdcvf12.pk"
  "Data": "./data/BTC-USD.csv",
  "StartDate": "2018-06-10",
  "EndDate": "2022-06-10",
  "Percentile25": 10,
  "Percentile50": 20,
  "BearMultiplier": 2,
  "Model": "PELT"
}
```

## Example output from Naive DCA Experiment
```
{ 
  "Data": "./data/BTC-USD.csv",
  "StartDate": "2018-06-10",
  "EndDate": "2022-06-10",
  "DaysRecurring": 14,
  "FixedAmount": 100,
  "Model": "NaiveDCA"
}
```

For detailed instructions on how to run these scripts, see the [documentation](https://docs.cloudera.com/machine-learning/cloud/models/topics/ml-creating-and-deploying-a-model.html).

