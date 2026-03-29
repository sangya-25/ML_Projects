import pandas as pd

# Load final cleaned dataset
df = pd.read_csv("silver_prices_final_full.csv")

# Ensure chronological order
df = df.sort_values('date').reset_index(drop=True)

# 1️⃣ Lag features (fill NaN with first available value)
for lag in [1,2,3]:
    df[f'price_inr_per_g_lag_{lag}'] = df['price_inr_per_g'].shift(lag)
    df[f'volume_lag_{lag}'] = df['volume'].shift(lag)

# Fill initial NaNs in lag features with first non-null value
for col in df.columns:
    if 'lag' in col:
        df[col].fillna(method='bfill', inplace=True)

# 2️⃣ Rolling / Moving averages (use min_periods=1 to avoid NaNs)
df['ma_3'] = df['price_inr_per_g'].rolling(window=3, min_periods=1).mean()
df['ma_7'] = df['price_inr_per_g'].rolling(window=7, min_periods=1).mean()
df['ma_14'] = df['price_inr_per_g'].rolling(window=14, min_periods=1).mean()

# 3️⃣ Rolling std (fill initial NaNs with 0)
df['std_7'] = df['price_inr_per_g'].rolling(window=7, min_periods=1).std().fillna(0)

# 4️⃣ Daily returns / percentage change (fill first row with 0)
df['return_pct'] = df['price_inr_per_g'].pct_change().fillna(0) * 100

# 5️⃣ Time features
df['day_of_week'] = pd.to_datetime(df['date']).dt.dayofweek
df['month'] = pd.to_datetime(df['date']).dt.month

# No dropna — we now preserve all rows
df = df.reset_index(drop=True)

# Save dataset with features
df.to_csv("silver_prices_features_fixed.csv", index=False)
print("Feature engineering complete! Saved as silver_prices_features_fixed.csv")
