import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV, TimeSeriesSplit
from sklearn.metrics import mean_squared_error
import joblib

# -------------------------
# 1️⃣ Load feature-engineered dataset
# -------------------------
df = pd.read_csv("silver_prices_features_fixed.csv")
df = df.sort_values('date').reset_index(drop=True)

# -------------------------
# 2️⃣ Features and target
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
# 3️⃣ Train/test split (chronological)
# -------------------------
train_size = int(len(df) * 0.8)
X_train = X[:train_size]
y_train = y[:train_size]
X_test = X[train_size:]
y_test = y[train_size:]

# -------------------------
# 4️⃣ Feature scaling (optional)
# -------------------------
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

print(f"Train shape: {X_train.shape}, Test shape: {X_test.shape}")
print("Data preparation complete. Ready for Random Forest training.")

# -------------------------
# 5️⃣ Hyperparameter tuning
# -------------------------
param_grid = {
    'n_estimators': [200, 300],
    'max_depth': [10, 15, None],
    'min_samples_split': [2, 5],
    'min_samples_leaf': [1, 2],
    'max_features': ['sqrt', 'log2', None]
}

tscv = TimeSeriesSplit(n_splits=5)
rf = RandomForestRegressor(random_state=42)

grid_search = GridSearchCV(
    estimator=rf,
    param_grid=param_grid,
    cv=tscv,
    scoring='neg_mean_squared_error',
    n_jobs=-1,
    verbose=1
)

grid_search.fit(X_train_scaled, y_train)

# -------------------------
# 6️⃣ Train final model
# -------------------------
best_rf = grid_search.best_estimator_
best_rf.fit(X_train_scaled, y_train)

# -------------------------
# 7️⃣ Predictions
# -------------------------
y_pred_train = best_rf.predict(X_train_scaled)
y_pred_test = best_rf.predict(X_test_scaled)

# -------------------------
# 8️⃣ Manual RMSE computation
# -------------------------
rmse_train = np.sqrt(mean_squared_error(y_train, y_pred_train))
rmse_test = np.sqrt(mean_squared_error(y_test, y_pred_test))

print(f"Train RMSE: {rmse_train:.2f} INR/g")
print(f"Test RMSE: {rmse_test:.2f} INR/g")

# -------------------------
# 9️⃣ Save trained model
# -------------------------
joblib.dump(best_rf, 'silver_price_rf_model.pkl')
print("Trained Random Forest model saved as silver_price_rf_model.pkl")
