import pandas as pd
import numpy as np

# Load dataset
df = pd.read_csv("silver_prices_clean.csv")

# Rename columns
df.rename(columns={
    'Date': 'date',
    'Close/Last': 'price_usd',
    'Open': 'open_usd',
    'High': 'high_usd',
    'Low': 'low_usd',
    'Volume': 'volume',
    'Change %': 'change_pct'
}, inplace=True)

# Convert date
df['date'] = pd.to_datetime(df['date'], format='%d/%m/%Y', errors='coerce')

# Drop rows where price is missing
df = df.dropna(subset=['price_usd'])

# Fill missing volume with median
median_volume = df['volume'].median()
df['volume'] = df['volume'].fillna(median_volume)

# Fill missing change_pct
if 'change_pct' in df.columns:
    df['change_pct'] = pd.to_numeric(df['change_pct'].str.replace('%','', regex=False), errors='coerce')
    df['change_pct'] = df['change_pct'].fillna(0)

# Sort chronologically
df = df.sort_values('date').reset_index(drop=True)

# Convert prices USD/oz → INR/g
usd_to_inr = 83.5
oz_to_g = 31.1035
for col in ['price_usd', 'open_usd', 'high_usd', 'low_usd']:
    df[col.replace('_usd', '_inr_per_g')] = df[col] * usd_to_inr / oz_to_g

# Save final cleaned dataset
df.to_csv("silver_prices_final_full.csv", index=False)
print("Preprocessing complete! Saved as silver_prices_final_full.csv")
