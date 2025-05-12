import pandas as pd
import pandas_datareader.data as web
import matplotlib.pyplot as plt
import statsmodels.api as sm
import pandas_datareader as pdr
import numpy as np

# set the gdp code and the start and end dates for the data
gdp_code = 'NGDPRSAXDCGBQ' #the UK
start_date = '1955-01-01'
end_date = '2022-01-01'

# download the data from FRED using pandas_datareader
gdp = web.DataReader(gdp_code, 'fred', start_date, end_date)
log_gdp = np.log(gdp)

# apply a Hodrick-Prescott filter to the data to extract the cyclical component
lambdas = [10, 100, 1600]
trends = {}
cycles = {}

for lam in lambdas:
    cycle, trend = sm.tsa.filters.hpfilter(log_gdp, lamb=lam)
    trends[lam] = trend
    cycles[lam] = cycle

# analyze the impact of different lambda values
for lam in lambdas:
    print(f"Cycle(λ={lam}) summary:")
    print(cycles[lam].describe())

    print(f"Trend(λ={lam}) summary:")
    print(trends[lam].describe())
