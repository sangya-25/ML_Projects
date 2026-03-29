import pandas as pd
import numpy as np

# === 1. Load raw CSV ===
df = pd.read_csv("silver_prices.csv")

print("Raw data loaded ✅")
print(df.head(), "\n")

# === 2. Standardize column names ===
df.columns = ['date', 'price', 'open', 'high', 'low', 'volume', 'change_%']

# === 3. Convert 'Date' to datetime ===
df['date'] = pd.to_datetime(df['date'], format='%d-%m-%Y', errors='coerce')

# === 4. Clean 'Change %' column ===
# Remove '%' and convert to float
df['change_%'] = df['change_%'].astype(str).str.replace('%', '').astype(float)

# === 5. Clean 'Volume' column ===
# Convert '32.08K', '1.64M' → numeric (K = thousand, M = million)
def parse_volume(val):
    if isinstance(val, str):
        val = val.replace(',', '').strip()
        if val.endswith('K'):
            return float(val[:-1]) * 1_000
        elif val.endswith('M'):
            return float(val[:-1]) * 1_000_000
        else:
            try:
                return float(val)
            except:
                return np.nan
    return val

df['volume'] = df['volume'].apply(parse_volume)

# === 6. Drop missing values ===
df = df.dropna()

# === 7. Sort chronologically (oldest → newest) ===
df = df.sort_values(by='date')

# === 8. Convert USD/oz → INR/g ===
USD_TO_INR = 83.0       # approx conversion (update later if needed)
OZ_TO_GRAM = 31.1035

for col in ['price', 'open', 'high', 'low']:
    df[f'{col}_inr_per_g'] = df[col] * USD_TO_INR / OZ_TO_GRAM

# === 9. Select relevant columns ===
final_df = df[['date', 'price_inr_per_g', 'open_inr_per_g', 'high_inr_per_g', 'low_inr_per_g', 'change_%', 'volume']]

# === 10. Save cleaned dataset ===
final_df.to_csv("cleaned_silver_data.csv", index=False)

print("✅ Cleaned data saved as 'cleaned_silver_data.csv'")
print(final_df.head())
