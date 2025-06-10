import pandas as pd
import pandas_datareader.data as web
import matplotlib.pyplot as plt
import statsmodels.api as sm
import pandas_datareader as pdr
import numpy as np


# Set the GDP codes and the start and end dates for the data
uk_gdp_code = 'NGDPRSAXDCGBQ' #the UK
jp_gdp_code = 'JPNRGDPEXP'
start_date = '1994-01-01'
end_date = '2022-01-01'


# Download the data from FRED using pandas_datareader
# UK
uk_gdp = web.DataReader(uk_gdp_code, 'fred', start_date, end_date)
uk_log_gdp = np.log(uk_gdp)

#Japan
jp_gdp = web.DataReader(jp_gdp_code, 'fred', start_date, end_date)
jp_log_gdp = np.log(jp_gdp)


# apply a Hodrick-Prescott filter to the data to extract the cyclical component
#UK
uk_cycle, uk_trend = sm.tsa.filters.hpfilter(uk_log_gdp, lamb=1600) #リポジトリにあるuk_business_cycle.pyで、lamb=10, 100, 1600を比較の上、1600を選択。

#Japan
jp_cycle, jp_trend = sm.tsa.filters.hpfilter(jp_log_gdp, lamb=1600)


# Compute statistics
# Standard deviations of cyclical components
uk_std = uk_cycle.std()
jp_std = jp_cycle.std()
# Correlation coefficient between UK and Japan cycles
corr = uk_cycle.corr(jp_cycle)


# Display standard deviations
print('--- 循環成分の標準偏差 ---')
print(f'  UK     : {uk_std:.4f}')
print(f'  Japan  : {jp_std:.4f}\n')

# Display correlation coefficient
print('--- UKとJapanの循環成分の相関係数 ---')
print(f'r = {corr:.4f}')


# Plot cyclical components
plt.figure(figsize=(10, 6))
plt.plot(uk_cycle.index, uk_cycle, label='UK Cycle (HP filter)')
plt.plot(jp_cycle.index, jp_cycle, label='Japan Cycle (HP filter)')
plt.title('HP-Filtered Cyclical Components of Real GDP\n(Quarterly, log scale)')
plt.xlabel('Date')
plt.ylabel('Deviation from Trend (log)')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.show()