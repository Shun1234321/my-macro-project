import pandas as pd
import numpy as np

# Load Penn World Table 9.0 data from the GGDC website
pwt90 = pd.read_stata('https://www.rug.nl/ggdc/docs/pwt90.dta')

# Define the list of OECD countries to include in the analysis
oecd_countries = [
    "Australia", "Austria", "Belgium", "Canada", "Denmark", "Finland",
    "France", "Germany", "Greece", "Iceland", "Ireland", "Italy", "Japan",
    "Netherlands", "New Zealand", "Norway", "Portugal", "Spain", "Sweden",
    "Switzerland", "United Kingdom", "United States"
]

# Filter data for selected countries and the period 1990–2019
data = pwt90[
    pwt90['country'].isin(oecd_countries) &
    pwt90['year'].between(1990, 2019)
]

# Select relevant columns and drop any rows with missing values
relevant_cols = ['countrycode', 'country', 'year', 'rgdpna', 'rkna', 'pop', 'emp', 'avh', 'labsh', 'rtfpna']
data = data[relevant_cols].dropna()



# === Variable-alpha version ===

# Calculate a country-specific capital share (alpha) as 1 minus the labor share
data['alpha_var'] = 1 - data['labsh']

data['hours'] = data['emp'] * data['avh'] # L
data['y_l']   = data['rgdpna'] / data['hours'] # Y/L
data['lab_term'] = data['hours'] / data['pop']  # L/N

# Take natural logs of variables for growth accounting
data['ln_y']  = np.log(data['y_l']) # ln(Y/L)
data['ln_k'] = np.log(data['rkna'] / data['hours']) # ln(K/L)
data['ln_a'] = data['ln_y'] - data['alpha_var'] * data['ln_k'] # ln(A)

# Compute annual changes (approximate growth rates) of the log variables
data['g_y'] = data.groupby('countrycode')['ln_y'].diff()  # ΔlnY/L
data['g_k'] = data.groupby('countrycode')['ln_k'].diff()  # ΔlnK/L
data['g_a'] = data.groupby('countrycode')['ln_a'].diff()  # ΔlnA



def calculate_growth_rates(country_data):
   
    # Calculate average annual growth rates and growth accounting shares over the full sample period for one country.
    start = country_data.iloc[0]
    end = country_data.iloc[-1]
    n_years = end['year'] - start['year']

    g_y = (end['ln_y'] - start['ln_y']) / n_years * 100
    g_k = (end['ln_k'] - start['ln_k']) / n_years * 100
    g_a = (end['ln_a'] - start['ln_a']) / n_years * 100

    alpha = country_data['alpha_var'].mean()
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


# Apply the growth accounting function to each country
results_df = data.groupby('country').apply(calculate_growth_rates)
results_df = results_df.reset_index().rename(columns={'country': 'Country'})

# Compute the cross-country average of each metric
avg_row_data = {
    'Country': 'Average',
    'Growth Rate': round(results_df['Growth Rate'].mean(), 2),
    'TFP Growth': round(results_df['TFP Growth'].mean(), 2),
    'Capital Deepening': round(results_df['Capital Deepening'].mean(), 2),
    'TFP Share': round(results_df['TFP Share'].mean(), 2),
    'Capital Share': round(results_df['Capital Share'].mean(), 2)
}
results_df = pd.concat([results_df, pd.DataFrame([avg_row_data])], ignore_index=True)

# Display the variable-alpha growth accounting table
print("\nGrowth Accounting in OECD Countries: 1990-2019 period (alpha_var)")
print("="*85)
print(results_df.to_string(index=False))





# === Fixed-alpha (0.3) version ===

# Set the capital share (alpha) to a constant 0.3 for all observations
data['alpha_fixed'] = 0.3

# Recompute labor hours, output per hour, and labor term (L/N)
data['hours'] = data['emp'] * data['avh'] # L
data['y_l']   = data['rgdpna'] / data['hours'] # Y/L
data['lab_term'] = data['hours'] / data['pop']  # L/N

# Take logs with fixed alpha
data['ln_y']  = np.log(data['y_l']) # ln(Y/L)
data['ln_k'] = np.log(data['rkna'] / data['hours']) # ln(K/L)
data['ln_a'] = data['ln_y'] - data['alpha_fixed'] * data['ln_k'] # ln(A)

# Compute annual changes again
data['g_y'] = data.groupby('countrycode')['ln_y'].diff()  # ΔlnY/L
data['g_k'] = data.groupby('countrycode')['ln_k'].diff()  # ΔlnK/L
data['g_a'] = data.groupby('countrycode')['ln_a'].diff()  # ΔlnA



def calculate_growth_rates(country_data):
   
   #Calculate average annual growth rates and growth accounting shares for the fixed-alpha case.
    start = country_data.iloc[0]
    end = country_data.iloc[-1]
    n_years = end['year'] - start['year']

    g_y = (end['ln_y'] - start['ln_y']) / n_years * 100
    g_k = (end['ln_k'] - start['ln_k']) / n_years * 100
    g_a = (end['ln_a'] - start['ln_a']) / n_years * 100

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


# Apply the fixed-alpha growth accounting function
results_df = data.groupby('country').apply(calculate_growth_rates)
results_df = results_df.reset_index().rename(columns={'country': 'Country'})

# Compute the average row for fixed-alpha results
avg_row_data = {
    'Country': 'Average',
    'Growth Rate': round(results_df['Growth Rate'].mean(), 2),
    'TFP Growth': round(results_df['TFP Growth'].mean(), 2),
    'Capital Deepening': round(results_df['Capital Deepening'].mean(), 2),
    'TFP Share': round(results_df['TFP Share'].mean(), 2),
    'Capital Share': round(results_df['Capital Share'].mean(), 2)
}
results_df = pd.concat([results_df, pd.DataFrame([avg_row_data])], ignore_index=True)

# Display the fixed-alpha growth accounting table
print("\nGrowth Accounting in OECD Countries: 1990-2019 period (alpha fixed)")
print("="*85)
print(results_df.to_string(index=False))

#comment
print("【考えたこと】αを変動させると、TFP成長がマイナスになる国が多い。\n安定的、整合的に国ごとで比較したい場合は、αは固定した方が良いと考えた。")