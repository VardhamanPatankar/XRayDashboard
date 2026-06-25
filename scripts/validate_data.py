import pandas as pd

df = pd.read_excel("data/prediction_logs_25062026.xlsx")

print("Total Rows:", len(df))
print("Total Columns:", len(df.columns))

print("\nMissing Values:\n")

print(df.isnull().sum())