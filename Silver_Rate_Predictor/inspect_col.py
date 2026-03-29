# inspect_columns.py
import pandas as pd
pd.set_option("display.max_columns", None)

csv_path = "silver_prices.csv"
df = pd.read_csv(csv_path)

print("=== Columns ===")
print(list(df.columns))
print("\n=== dtypes ===")
print(df.dtypes)
print("\n=== First 8 rows ===")
print(df.head(8))
