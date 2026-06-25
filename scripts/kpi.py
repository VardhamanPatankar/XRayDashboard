import pandas as pd

# Read data
df = pd.read_excel("data/prediction_logs_25062026.xlsx")

# Total X-rays
total_xrays = len(df)

# Normal cases
normal_cases = len(
    df[df["flag_abnormal"] == "no"]
)

# Abnormal cases
abnormal_cases = len(
    df[df["flag_abnormal"] == "yes"]
)

# Abnormality %
abnormality_pct = (
    abnormal_cases / total_xrays
) * 100

# Clinics processed
clinics_processed = (
    df["cust_id"].nunique()
)

print("\n===== DAILY KPI SUMMARY =====\n")

print("Total X-rays:", total_xrays)

print("Normal Cases:", normal_cases)

print("Abnormal Cases:", abnormal_cases)

print(
    f"Abnormality %: {abnormality_pct:.2f}%"
)

print(
    "Clinics Processed:",
    clinics_processed
)