import pandas as pd

# --------------------
# Load Data
# --------------------

df = pd.read_excel(
    "data/prediction_logs_25062026.xlsx"
)

# --------------------
# Disease Classification
# --------------------

def classify_disease(text):

    text = str(text).lower()

    if "normal" in text:
        return "Normal"

    elif "nodule" in text:
        return "Nodule"

    elif "fracture" in text:
        return "Fracture"

    elif "osteoarthritis" in text:
        return "Osteoarthritis"

    elif (
        "joint space narrowing" in text
        or "degenerative joint disease" in text
    ):
        return "Joint Disease"

    elif (
        "fecal loading" in text
        or "bowel" in text
    ):
        return "Gastrointestinal"

    else:
        return "Others"

df["disease_category"] = (
    df["pred_summary"]
    .apply(classify_disease)
)

# --------------------
# KPI Summary
# --------------------

total_xrays = len(df)

normal_cases = len(
    df[df["flag_abnormal"] == "no"]
)

abnormal_cases = len(
    df[df["flag_abnormal"] == "yes"]
)

abnormality_pct = (
    abnormal_cases / total_xrays
) * 100

clinics_processed = (
    df["cust_id"].nunique()
)

kpi_summary = pd.DataFrame({
    "Metric": [
        "Total X-rays",
        "Normal Cases",
        "Abnormal Cases",
        "Abnormality %",
        "Clinics Processed"
    ],
    "Value": [
        total_xrays,
        normal_cases,
        abnormal_cases,
        round(abnormality_pct, 2),
        clinics_processed
    ]
})

# --------------------
# Disease Summary
# --------------------

disease_summary = (
    df["disease_category"]
    .value_counts()
    .reset_index()
)

disease_summary.columns = [
    "Disease",
    "Count"
]

# --------------------
# Clinic Summary
# --------------------

clinic_summary = (
    df.groupby("cust_id")
    .agg(
        studies=("cust_id", "count")
    )
)

normal_cases_clinic = (
    df[df["flag_abnormal"] == "no"]
    .groupby("cust_id")
    .size()
)

abnormal_cases_clinic = (
    df[df["flag_abnormal"] == "yes"]
    .groupby("cust_id")
    .size()
)

clinic_summary["normal_cases"] = normal_cases_clinic
clinic_summary["abnormal_cases"] = abnormal_cases_clinic

clinic_summary = clinic_summary.fillna(0)

clinic_summary["abnormal_pct"] = (
    clinic_summary["abnormal_cases"]
    / clinic_summary["studies"]
) * 100

clinic_summary = clinic_summary.reset_index()

# --------------------
# Excel Report
# --------------------

with pd.ExcelWriter(
    "reports/daily_report.xlsx"
) as writer:

    kpi_summary.to_excel(
        writer,
        sheet_name="KPI Summary",
        index=False
    )

    disease_summary.to_excel(
        writer,
        sheet_name="Disease Statistics",
        index=False
    )

    clinic_summary.to_excel(
        writer,
        sheet_name="Clinic Statistics",
        index=False
    )

print(
    "Excel report generated successfully!"
)