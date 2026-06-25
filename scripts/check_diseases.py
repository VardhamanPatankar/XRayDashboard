import pandas as pd

df = pd.read_excel("data/prediction_logs_25062026.xlsx")

for i, value in enumerate(df["pred_summary"].unique(), start=1):
    print(f"\n{i}. {value}")