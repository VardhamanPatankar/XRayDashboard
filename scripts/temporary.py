import pandas as pd

df = pd.read_excel("data/prediction_logs_25062026.xlsx")

print(df["timestamp.1"].head())