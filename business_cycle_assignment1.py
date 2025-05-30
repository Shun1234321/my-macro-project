import pandas as pd
import pandas_datareader.data as web
import matplotlib.pyplot as plt
import statsmodels.api as sm
import pandas_datareader as pdr
import numpy as np


# set the gdp code and the start and end dates for the data
uk_gdp_code = 'NGDPRSAXDCGBQ' #the UK
jp_gdp_code = 'JPNRGDPEXP'
start_date = '1955-01-01'
end_date = '2022-01-01'


# download the data from FRED using pandas_datareader
#UK
uk_gdp = web.DataReader(uk_gdp_code, 'fred', start_date, end_date)
uk_log_gdp = np.log(uk_gdp)

#JP
jp_gdp = web.DataReader(jp_gdp_code, 'fred', start_date, end_date)
jp_log_gdp = np.log(jp_gdp)


# apply a Hodrick-Prescott filter to the data to extract the cyclical component
#UK
uk_cycle, uk_trend = sm.tsa.filters.hpfilter(uk_log_gdp, lamb=1600)

#JP
jp_cycle, jp_trend = sm.tsa.filters.hpfilter(jp_log_gdp, lamb=1600)



