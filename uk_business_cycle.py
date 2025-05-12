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


#-----trends-----
# Prepare the figure for plotting
plt.figure(figsize=(12,6))

# Plot the original time series data
plt.plot(log_gdp, label="Original GDP (in log)")

# Plot the trend components
for lam in lambdas:
    plt.plot(trends[lam], label=f"Trend (λ={lam})")

# Add a legend, labels, and a title
plt.legend()
plt.xlabel("Date")
plt.ylabel("Log of real GDP")
plt.title("Comparison of Original Data and Trend Components")


# -----cycles-----
# Prepare the figure for plotting
plt.figure(figsize=(12,6))

# Plot the cycle components
for lam in lambdas:
    plt.plot(cycles[lam], label=f"Cycle (λ={lam})")

# Add a legend, labels, and a title
plt.legend()
plt.xlabel("Date")
plt.ylabel("Cyclical Component")
plt.title("Comparison of Cyclical Components with Different Lambda Values")


# show the plot
plt.show()