import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

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
# 4️⃣ Feature scaling (same as training)
# -------------------------
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# -------------------------
# 5️⃣ Load trained Random Forest model
# -------------------------
rf_model = joblib.load('silver_price_rf_model.pkl')

# -------------------------
# 6️⃣ Predictions
# -------------------------
y_pred_train = rf_model.predict(X_train_scaled)
y_pred_test = rf_model.predict(X_test_scaled)

# -------------------------
# 7️⃣ Evaluation metrics
# -------------------------
rmse_train = np.sqrt(mean_squared_error(y_train, y_pred_train))
rmse_test = np.sqrt(mean_squared_error(y_test, y_pred_test))

mae_train = mean_absolute_error(y_train, y_pred_train)
mae_test = mean_absolute_error(y_test, y_pred_test)

r2_train = r2_score(y_train, y_pred_train)
r2_test = r2_score(y_test, y_pred_test)

print(f"Train RMSE: {rmse_train:.2f} INR/g")
print(f"Test RMSE: {rmse_test:.2f} INR/g")
print(f"Train MAE: {mae_train:.2f} INR/g")
print(f"Test MAE: {mae_test:.2f} INR/g")
print(f"Train R²: {r2_train:.3f}")
print(f"Test R²: {r2_test:.3f}")

# -------------------------
# 8️⃣ Plot Predicted vs Actual
# -------------------------
plt.figure(figsize=(12,6))
plt.plot(y_test.values, label='Actual', color='blue')
plt.plot(y_pred_test, label='Predicted', color='red', alpha=0.7)
plt.xlabel("Time Steps")
plt.ylabel("Silver Price (INR/g)")
plt.title("Silver Price Prediction vs Actual")
plt.legend()
plt.show()

# -------------------------
# 9️⃣ Plot Feature Importance
# -------------------------
importances = rf_model.feature_importances_
plt.figure(figsize=(10,6))
plt.barh(feature_cols, importances)
plt.xlabel("Feature Importance")
plt.title("Random Forest Feature Importance")
plt.show()
