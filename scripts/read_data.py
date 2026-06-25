import pandas as pd

# Read Excel file
df = pd.read_excel("data/prediction_logs_25062026.xlsx")

# Show first 5 rows
print(df.head())

print("\n-------------------")
print("Columns:")
print(df.columns)