import pandas as pd
from sklearn.preprocessing import StandardScaler

# -------------------------
# Load feature-engineered dataset
# -------------------------
df = pd.read_csv("silver_prices_features_fixed.csv")

# Ensure chronological order
df = df.sort_values('date').reset_index(drop=True)

# -------------------------
# Select features and target
# -------------------------
feature_cols = [
    'price_inr_per_g_lag_1', 'price_inr_per_g_lag_2', 'price_inr_per_g_lag_3',
    'volume', 'volume_lag_1', 'volume_lag_2', 'volume_lag_3',
    'ma_3', 'ma_7', 'ma_14', 'std_7', 'return_pct', 'day_of_week', 'month'
]
target_col = 'price_inr_per_g'

X = df[feature_cols]
y = df[target_col]

# -------------------------
# Chronological train/test split
# -------------------------
train_size = int(len(df) * 0.8)
X_train = X[:train_size]
y_train = y[:train_size]
X_test = X[train_size:]
y_test = y[train_size:]

print(f"Train shape: {X_train.shape}, Test shape: {X_test.shape}")

# -------------------------
# Feature scaling (optional)
# -------------------------
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

print("Data preparation complete. Ready for Random Forest training.")
