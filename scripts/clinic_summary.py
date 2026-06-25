import pandas as pd

df = pd.read_excel(
    "data/prediction_logs_25062026.xlsx"
)

summary = (
    df.groupby("cust_id")
      .agg(
          studies=("cust_id", "count")
      )
)

normal_cases = (
    df[df["flag_abnormal"] == "no"]
    .groupby("cust_id")
    .size()
)

abnormal_cases = (
    df[df["flag_abnormal"] == "yes"]
    .groupby("cust_id")
    .size()
)

summary["normal_cases"] = normal_cases
summary["abnormal_cases"] = abnormal_cases

summary = summary.fillna(0)

summary["abnormal_pct"] = (
    summary["abnormal_cases"]
    / summary["studies"]
) * 100

summary = summary.reset_index()

print(summary)