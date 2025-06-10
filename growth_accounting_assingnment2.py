import pandas as pd
import numpy as np

pwt90 = pd.read_stata('https://www.rug.nl/ggdc/docs/pwt90.dta')

oecd_countries = [
    "Australia", "Austria", "Belgium", "Canada", "Denmark", "Finland",
    "France", "Germany", "Greece", "Iceland", "Ireland", "Italy", "Japan",
    "Netherlands", "New Zealand", "Norway", "Portugal", "Spain", "Sweden",
    "Switzerland", "United Kingdom", "United States"
]

data = pwt90[
    pwt90['country'].isin(oecd_countries) &
    pwt90['year'].between(1990, 2019)
]

relevant_cols = ['countrycode', 'country', 'year', 'rgdpna', 'rkna', 'pop', 'emp', 'avh', 'labsh', 'rtfpna']
data = data[relevant_cols].dropna()

# Calculate additional variables
# αを固定値0.3に設定
data['alpha_fixed'] = 0.3

data['hours'] = data['emp'] * data['avh'] # 労働時間 L
data['y_l']   = data['rgdpna'] / data['hours'] # Y/L：１時間あたりの付加価値
data['lab_term'] = data['hours'] / data['pop']  # L/N

# 対数を取る
data['ln_y']  = np.log(data['y_l']) # ln(Y/L)
data['ln_k'] = np.log(data['rkna'] / data['hours']) # ln(K/L)
data['ln_a'] = data['ln_y'] - data['alpha_fixed'] * data['ln_k'] # ln(A)

# 2) 年次差分（≒成長率）を取る
data['g_y'] = data.groupby('countrycode')['ln_y'].diff()  # ΔlnY/L
data['g_k'] = data.groupby('countrycode')['ln_k'].diff()  # ΔlnK/L
data['g_a'] = data.groupby('countrycode')['ln_a'].diff()  # ΔlnA



def calculate_growth_rates(country_data):
   
    g_y = country_data['g_y'].mean() * 100
    g_k = country_data['g_k'].mean() * 100
    g_a = country_data['g_a'].mean() * 100

    alpha = country_data['alpha_fixed'].iloc[0]
    capital_deepening_contrib = alpha * g_k
    tfp_growth_calculated = g_a
    
    tfp_share = (tfp_growth_calculated / g_y)
    cap_share = (capital_deepening_contrib / g_y)

    return  pd.Series({
        'Growth Rate': round(g_y, 2),
        'TFP Growth': round(tfp_growth_calculated, 2),
        'Capital Deepening': round(capital_deepening_contrib, 2),
        'TFP Share': round(tfp_share, 2),
        'Capital Share': round(cap_share, 2)
    })


results_df = data.groupby('country').apply(calculate_growth_rates)
results_df = results_df.reset_index().rename(columns={'country': 'Country'})

avg_row_data = {
    'Country': 'Average',
    'Growth Rate': round(results_df['Growth Rate'].mean(), 2),
    'TFP Growth': round(results_df['TFP Growth'].mean(), 2),
    'Capital Deepening': round(results_df['Capital Deepening'].mean(), 2),
    'TFP Share': round(results_df['TFP Share'].mean(), 2),
    'Capital Share': round(results_df['Capital Share'].mean(), 2)
}
results_df = pd.concat([results_df, pd.DataFrame([avg_row_data])], ignore_index=True)

print("\nGrowth Accounting in OECD Countries: 1990-2019 period")
print("="*85)
print(results_df.to_string(index=False))

