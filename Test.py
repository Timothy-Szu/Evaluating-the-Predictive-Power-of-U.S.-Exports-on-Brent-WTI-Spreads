import requests
import numpy as np
import pandas as pd
import yfinance as yf
from functools import reduce
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns
#=============================================================================
# Instructions :
# 1. Uncomment each section and run it individually
# 2. Comment it out again before running another section
#=============================================================================
# Store our EIA API urls
urls = {
    "cushing_stocks": "https://api.eia.gov/v2/petroleum/stoc/wstk/data/?api_key=mHCNlUj4y2kuYwV3bMFWdUPh10PB7wqCrjaGL7CI&frequency=weekly&data[0]=value&facets[series][]=W_EPC0_SAX_YCUOK_MBBL&start=2016-01-01&sort[0][column]=period&sort[0][direction]=desc&offset=0&length=5000",
    "crude_exports": "https://api.eia.gov/v2/petroleum/move/wkly/data/?api_key=mHCNlUj4y2kuYwV3bMFWdUPh10PB7wqCrjaGL7CI&frequency=weekly&data[0]=value&facets[series][]=WCREXUS2&start=2005-01-01&sort[0][column]=period&sort[0][direction]=desc&offset=0&length=5000",
    "field_production": "https://api.eia.gov/v2/petroleum/sum/sndw/data/?api_key=mHCNlUj4y2kuYwV3bMFWdUPh10PB7wqCrjaGL7CI&frequency=weekly&data[0]=value&facets[series][]=WCRFPUS2&start=2016-01-01&sort[0][column]=period&sort[0][direction]=desc&offset=0&length=5000",
    "refinery_input": "https://api.eia.gov/v2/petroleum/sum/sndw/data/?api_key=mHCNlUj4y2kuYwV3bMFWdUPh10PB7wqCrjaGL7CI&frequency=weekly&data[0]=value&facets[series][]=WGIRIUS2&start=2016-01-01&sort[0][column]=period&sort[0][direction]=desc&offset=0&length=5000",
    "gulf_stocks": "https://api.eia.gov/v2/petroleum/stoc/wstk/data/?api_key=mHCNlUj4y2kuYwV3bMFWdUPh10PB7wqCrjaGL7CI&frequency=weekly&data[0]=value&facets[product][]=EPC0&facets[series][]=WCESTP31&sort[0][column]=period&sort[0][direction]=desc&offset=0&length=5000"
}

dfs = {}
# Process the urls 
for name, url in urls.items():
    res = requests.get(url)
    data = res.json()

    if "response" in data:
        df = pd.DataFrame(data["response"]["data"])
        df["value"] = pd.to_numeric(df["value"])
        dfs[name] = df
    else:
        raise ValueError(f"API error or unexpected format: {data}")
    
# Data Cleaning
renamed = []
for name, df in dfs.items():
    temp = df.copy()

    # Rename non-period columns to avoid collisions when merging
    cols = {
        col: f"{name}_{col}"
        for col in temp.columns
        if col != "period"
    }
    temp = temp.rename(columns=cols)
    renamed.append(temp)

# Merge Data
master_df = reduce(
    lambda left, right: pd.merge(left, right, on="period", how="outer"), renamed)
master_df['period'] = pd.to_datetime(master_df['period'])

#=============================================================================
# Process Yahoo Finance data and Merge with EIA 
prices = yf.download(["CL=F", "BZ=F"], start="2016-01-01")['Close']
prices_weekly = prices.resample('W-FRI').last()
#Simplification : Use friday closing prices to reduce noise
prices_weekly = prices_weekly.rename(columns={'BZ=F': 'Brent', 'CL=F': 'WTI'})
prices_weekly['spread'] = prices_weekly['Brent'] - prices_weekly['WTI']
prices_weekly.index = pd.to_datetime(prices_weekly.index)
master_df = pd.merge(master_df, prices_weekly, left_on='period', right_index=True, how='inner')

#=============================================================================
#Check the data
#print(master_df.info())
#print(master_df.head())

#=============================================================================
#Useful preliminary calculations
master_df['production_mmbpd'] = master_df['field_production_value'] / 1000
master_df['exports_mmbpd'] = master_df['crude_exports_value'] / 1000
master_df['refinery_runs_mmbpd'] = master_df['refinery_input_value'] / 1000
master_df['domestic_surplus'] = master_df['production_mmbpd'] - master_df['refinery_runs_mmbpd']
master_df['export_efficiency'] = master_df['exports_mmbpd'] / master_df['production_mmbpd']
df_clean = master_df[['period', 'spread', 'cushing_stocks_value','gulf_stocks_value', 'domestic_surplus', 'export_efficiency','exports_mmbpd']].copy()
df_clean.set_index('period', inplace=True)

#=============================================================================

# US Exports Visualization, Figure 1
# The Surge of U.S. Crude Oil Exports (2005–2026)
"""
df_temp = pd.DataFrame()
df_temp = dfs["crude_exports"].copy()
# Use data from 2005 and onwards
df_temp["period"] = pd.to_datetime(df_temp["period"])
df_temp = df_temp.set_index("period").sort_index()
df_temp = df_temp.loc["2005-01-01":]

# 1. Setup the figure
plt.figure(figsize=(12, 6), dpi=150)
plt.style.use('seaborn-v0_8-whitegrid')

# 2. Plot the Export Data
plt.plot(df_temp.index, df_temp["value"], color='#004a99', linewidth=2, label='U.S. Crude Exports')

# 3. Add the 2015 Policy Shift line
# Most export data really takes off after Dec 2015
plt.axvline(pd.to_datetime('2015-12-18'), color='#d9534f', linestyle='--', linewidth=1.5)
plt.text(pd.to_datetime('2016-03-01'), plt.ylim()[1]*0.8, 'Export Ban Lifted\n(Dec 2015)', 
         color='#d9534f', fontweight='bold', fontsize=10)

# 4. Styling
plt.title("The Surge of U.S. Crude Oil Exports (2005–2026)", fontsize=16, pad=20, fontweight='bold')
plt.ylabel("Barrels per Day (Thousand bbl/d)", fontsize=12)
plt.xlabel("Year", fontsize=12)
plt.axvspan(pd.to_datetime('2016-01-01'), df_clean.index[-1], color='gray', alpha=0.1, label='Post-Ban Regime')
plt.legend(loc='upper left')
plt.tight_layout()
plt.show()
"""
#=============================================================================
# Gulf and Cushing Inventory Correlations with Various Lags, Figure 2
# Time-Lag Correlation Sensitivity Analysis: Inventory vs Brent-WTI Spread
"""
# Dictionaries to store correlations
corr_dict = {
    'Gulf Stocks': [],
    'Cushing Stocks': []
}

df_normal = df_clean.loc[:'2026-01-01'].copy()
lags = list(range(25))

for lag in lags:
    corr_dict['Gulf Stocks'].append(df_normal['spread'].corr(df_normal['gulf_stocks_value'].shift(lag)))
    corr_dict['Cushing Stocks'].append(df_normal['spread'].corr(df_normal['cushing_stocks_value'].shift(lag)))

# Create the Plot
plt.figure(figsize=(12, 6), dpi=100)
sns.set_style("whitegrid")

# Plot both series
plt.plot(lags, corr_dict['Gulf Stocks'], marker='o', linestyle='-', color='#004a99', linewidth=2.5, markersize=8, label='Gulf Stocks')
plt.plot(lags, corr_dict['Cushing Stocks'], marker='s', linestyle='--', color='#ff7f0e', linewidth=2.5, markersize=8, label='Cushing Stocks')

# Highlight the 13-week 'Sweet Spot' for Gulf Stocks
plt.annotate(f'Peak Lead Indicator (13 Weeks) \nGulf Corr: {corr_dict["Gulf Stocks"][13]:.3f}', 
             xy=(13, corr_dict["Gulf Stocks"][13]-0.01), xytext=(15, corr_dict["Gulf Stocks"][12] -0.025 ),
             arrowprops=dict(facecolor='black', shrink=0.05),
             fontsize=12, fontweight='bold')

# Highlight the bottom plateau (The Transmission Window)
plt.axvspan(11, 14, color='green', alpha=0.15, label='Key Transmission Window')
plt.annotate('Logistical Lag Window (11-14 Weeks)', 
             xy=(12.5, min(corr_dict['Gulf Stocks'])), xytext=(12.5, min(corr_dict['Gulf Stocks']) + 0.1),
             ha='center', fontsize=10, fontweight='bold',
             arrowprops=dict(arrowstyle='->', color='black'))

# Styling
plt.title('Time-Lag Correlation Sensitivity Analysis: Inventory vs Brent-WTI Spread', fontsize=16, pad=20)
plt.xlabel('Lag (Weeks)', fontsize=12)
plt.ylabel('Pearson Correlation Coefficient (r)', fontsize=12)
plt.xticks(range(0, 25, 2))
plt.grid(True, which='both', linestyle='--', alpha=0.5)
plt.axhline(0, color='black', linewidth=1)

# Legend
plt.legend(fontsize=12, loc='upper left', bbox_to_anchor=(0, 0.95), frameon=True)               
plt.tight_layout()
plt.show()
"""

#=============================================================================
#Export Utilization Calculations for Subsequent Tests

#Simplification : Calculate a 52-week rolling maximum to estimate "Export Capacity"
df_clean['export_capacity_est'] = df_clean['exports_mmbpd'].rolling(window=52, min_periods=1).max()

# Calculate Export Utilization
df_clean['export_utilization'] = df_clean['exports_mmbpd'] / df_clean['export_capacity_est']

#=============================================================================
# Test Correlations under Export Utilization Regimes, Figure 3
# Sensitivity Analysis: Regime-Switching Robustness

"""
# Export utilization derived from most recent EIA Weekly Estimate (Released on Weds)
df_clean['export_utilization'] = df_clean['export_utilization'].shift(1)
results = []

for threshold in (0.8,0.9,0.95):
    for s in range(11,14,1):

        # Create lagged variable
        df_clean['gulf_lag'] = df_clean['gulf_stocks_value'].shift(s)
        df_lagged = df_clean.dropna(subset=['gulf_lag', 'export_utilization']).copy()

        # Split regimes
        high_mask = df_lagged['export_utilization'] > threshold

        df_high = df_lagged[high_mask]
        df_normal = df_lagged[~high_mask]

        corr_normal = df_normal['spread'].corr(df_normal['gulf_lag'])
        corr_high = df_high['spread'].corr(df_high['gulf_lag'])
   
        # Store results
        results.append({
            'Lag_Weeks': s,
            'Threshold': f">{threshold:.0%}",
            'Normal_Corr': round(corr_normal, 3),
            'High_Corr': round(corr_high, 3),
            'Normal_N': len(df_normal),
            'High_N': len(df_high)
        })

# Convert to DataFrame
results_df = pd.DataFrame(results)

# Print Results 
print("\n" + "="*50)
print("Sensitivity Analysis Table")
print("="*50)
print(results_df.to_string(index=False))
print("="*50)

# Pivot Table to Present Results
pivot_df = results_df.pivot(index='Threshold', columns='Lag_Weeks', values='High_Corr')
styled_table = pivot_df.style.background_gradient(cmap='Reds', axis=None) \
    .format("{:.3f}") \
    .set_caption("Sensitivity Analysis: Clogged Regime Correlation (r)")\
    .set_table_styles([
        {'selector': 'th', 'props': [('font-size', '12pt'), ('background-color', '#f7f7f7')]},
        {'selector': 'td', 'props': [('padding', '10px'), ('border', '1px solid #ddd')]}
    ])
# Heatmap to compare Thresholds vs Lags
plt.figure(figsize=(10, 4), dpi=150)
plt.rcParams['font.family'] = 'sans-serif'

# Deeper Shades of Red Indicate Stronger Magnitude of Correlation
ax = sns.heatmap(pivot_df, annot=True, fmt=".3f", cmap="YlOrRd_r", 
                 cbar_kws={'label': 'Correlation Strength (r)'},
                 linewidths=1, linecolor='white', annot_kws={"size": 12, "weight": "bold"})

# Styling
plt.title("Sensitivity Analysis: Regime-Switching Robustness", fontsize=16, pad=20, fontweight='bold')
plt.xlabel("Logistical Lag (Weeks)", fontsize=12, labelpad=10)
plt.ylabel("Utilization Threshold", fontsize=12, labelpad=10)

# Highlight the Strongest Correlation (The 11-week, 95% cell)
from matplotlib.patches import Rectangle
ax.add_patch(Rectangle((0,2), 1, 1, fill=False, edgecolor='blue', lw=4))
plt.tight_layout()
plt.show()
"""

#=============================================================================
# P-Value Test to Confirm Statistical Significance of Previous Correlation Findings
"""
# 11-week lag
df_clean['gulf_lag'] = df_clean['gulf_stocks_value'].shift(11)

df_test = df_clean.dropna(subset=['gulf_lag', 'export_utilization'])

# 95% utilization regime
df_high = df_test[df_test['export_utilization'] > 0.95]

r, p = stats.pearsonr(df_high['spread'], df_high['gulf_lag'])

print(f"Correlation: {r:.3f}")
print(f"P-value: {p:.5f}")
print(f"N: {len(df_high)}")
"""
#=============================================================================
# Back-Test Our Strategy, Figure 4
# Threshold Sensitivity & Resilience Analysis (2016 - 2026)
"""
# 1. Setup Strategy Parameters
lag = 11
holding_period = 4
start_date = '2016-01-01'
thresholds = [0.7, 0.80, 0.90, 0.95]
conflict_date = pd.to_datetime("2026-02-01")
colors = ['#3498db', '#f39c12', '#27ae60', '#132456']
plt.figure(figsize=(12, 7), dpi=150)

# 2. Filter data
bt_df = df_clean.loc[start_date:].copy()

# 3. Build the Inventory Signal
z_window = 52  # 52 weeks = 1 year

bt_df['rolling_mean'] = (bt_df['gulf_stocks_value'].rolling(z_window).mean())
bt_df['rolling_std'] = (bt_df['gulf_stocks_value'].rolling(z_window).std())
bt_df['z_inv_score'] = ((bt_df['gulf_stocks_value'] - bt_df['rolling_mean'])/ bt_df['rolling_std'])  

# High inventory condition
bt_df['inv_high'] = ( bt_df['z_inv_score'] > 1).astype(int)
bt_df['high_consecutive'] = (bt_df['inv_high'].rolling(3).sum().eq(3))

# Low inventory condition
bt_df['inv_low'] = (bt_df['z_inv_score'] < -1).astype(int)
bt_df['low_consecutive'] = (bt_df['inv_low'].rolling(3).sum().eq(3))

# Shift signal back 11 weeks
bt_df['high_inventory_signal'] = bt_df['high_consecutive'].shift(lag)
bt_df['low_inventory_signal']  = bt_df['low_consecutive'].shift(lag)

# 4. Future Spread Change (Using Friday Closing Price)
bt_df['future_spread_change'] = (bt_df['spread'].shift(-holding_period) - bt_df['spread'])

# 5. Back-Test 
for t, col in zip(thresholds, colors):
    # Export Utilization from Most Recent Weekly EIA Estimate (Released Weds)
    export_signal = bt_df['export_utilization'].shift(1) > t
    # Strategy condition
    short_condition = (bt_df['high_inventory_signal'] & export_signal)
    long_condition = (bt_df['low_inventory_signal'] & export_signal)

    # Short Brent-WTI
    bt_df[f'signal_{t}'] =  np.select([long_condition,short_condition],[1,-1],default=0)
    # PnL
    bt_df[f'pnl_{t}'] = (bt_df[f'signal_{t}'] *bt_df['future_spread_change']).fillna(0)
    bt_df[f'cum_pnl_{t}'] = bt_df[f'pnl_{t}'].cumsum()

    # Plot the result
    lw = 2 if t == 0.9 else 1.5
    alpha = 1.0 if t == 0.9 else 0.6
    plt.step(bt_df.index, bt_df[f'cum_pnl_{t}'], where='post', 
             color=col, linewidth=lw, alpha=alpha, label=f'Threshold: {int(t*100)}%')

# Styling
plt.axvline(conflict_date, color='#c0392b', linestyle='--', linewidth=2)
covid_date = pd.to_datetime("2020-03-01")
plt.axvline(covid_date, color='#c0392b', linestyle='--', linewidth=2)
ukraine_date = pd.to_datetime("2022-02-24")
plt.axvline(ukraine_date, color='#c0392b', linestyle='--', linewidth=2)

# Annotations
plt.text(pd.to_datetime('2026-02-28'), plt.ylim()[1]*0.65, 'Iran War\n2026', 
         color='#c0392b', fontweight='bold', ha='left')
plt.text(pd.to_datetime('2023-06-01'), plt.ylim()[1]*0.65, 'Geopolitical Regime', 
         color='#c0392b', fontweight='bold', ha='left')
plt.text(pd.to_datetime('2020-06-01'), plt.ylim()[1]*0.60, 'COVID-19 Regime', 
         color='#c0392b', fontweight='bold', ha='left')
plt.text(pd.to_datetime('2017-01-01'), plt.ylim()[1]*0.65, 'Export Regime', 
         color='#c0392b', fontweight='bold', ha='left')
plt.axhline(0, color='black', lw=0.8, alpha=0.5)

plt.title("Threshold Sensitivity & Resilience Analysis (2016 - 2026)", fontsize=16, fontweight='bold')
plt.ylabel("Cumulative Profit (USD per Spread)", fontsize=12)
plt.xlabel("Trade Date", fontsize=12)
plt.grid(True, alpha=0.2, linestyle='--')
plt.legend(loc='upper left', title="Utilization Cutoff")

plt.tight_layout()
plt.show()
"""
#============================================================================





