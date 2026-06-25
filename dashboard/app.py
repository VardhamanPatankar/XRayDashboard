import streamlit as st
import pandas as pd
import plotly.express as px

# --------------------
# Load Data
# --------------------

df = pd.read_excel(
    "data/prediction_logs_25062026.xlsx"
)

# --------------------
# Create Date Column
# --------------------

df["date"] = pd.to_datetime(
    df["timestamp.1"],
    format="%Y-%m-%d_%H:%M:%S"
).dt.date

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
# Sidebar Filters
# --------------------

st.sidebar.header("Filters")

customers = st.sidebar.multiselect(
    "Select Clinic",
    options=sorted(df["cust_id"].unique()),
    default=sorted(df["cust_id"].unique())
)

image_categories = st.sidebar.multiselect(
    "Select Image Category",
    options=sorted(df["image_category"].unique()),
    default=sorted(df["image_category"].unique())
)

outcomes = st.sidebar.multiselect(
    "Select Outcome",
    options=sorted(df["flag_abnormal"].unique()),
    default=sorted(df["flag_abnormal"].unique())
)

dates = st.sidebar.multiselect(
    "Select Date",
    options=sorted(df["date"].unique()),
    default=sorted(df["date"].unique())
)

# --------------------
# Apply Filters
# --------------------

filtered_df = df[
    (df["cust_id"].isin(customers))
    &
    (df["image_category"].isin(image_categories))
    &
    (df["flag_abnormal"].isin(outcomes))
    &
    (df["date"].isin(dates))
]

# --------------------
# Disease Summary
# --------------------

disease_summary = (
    filtered_df["disease_category"]
    .value_counts()
    .reset_index()
)

disease_summary.columns = [
    "Disease",
    "Count"
]

# --------------------
# Customer Summary
# --------------------

customer_summary = (
    filtered_df.groupby("cust_id")
    .size()
    .reset_index(name="Studies")
)

# --------------------
# Daily Trend
# --------------------

daily_trend = (
    filtered_df.groupby("date")
    .size()
    .reset_index(name="Studies")
)

# --------------------
# Clinic Summary
# --------------------

clinic_summary = (
    filtered_df.groupby("cust_id")
    .agg(
        studies=("cust_id", "count")
    )
)

normal_cases_clinic = (
    filtered_df[
        filtered_df["flag_abnormal"] == "no"
    ]
    .groupby("cust_id")
    .size()
)

abnormal_cases_clinic = (
    filtered_df[
        filtered_df["flag_abnormal"] == "yes"
    ]
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
# KPI Calculations
# --------------------

total_xrays = len(filtered_df)

normal_cases = len(
    filtered_df[
        filtered_df["flag_abnormal"] == "no"
    ]
)

abnormal_cases = len(
    filtered_df[
        filtered_df["flag_abnormal"] == "yes"
    ]
)

if total_xrays > 0:
    abnormality_pct = (
        abnormal_cases / total_xrays
    ) * 100
else:
    abnormality_pct = 0

clinics_processed = (
    filtered_df["cust_id"].nunique()
)

# --------------------
# Dashboard Title
# --------------------

st.title("X-Ray Analytics Dashboard")

# --------------------
# KPI Cards
# --------------------

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(
        "Total X-Rays",
        total_xrays
    )

with col2:
    st.metric(
        "Normal",
        normal_cases
    )

with col3:
    st.metric(
        "Abnormal",
        abnormal_cases
    )

with col4:
    st.metric(
        "Abnormal %",
        f"{abnormality_pct:.2f}%"
    )

with col5:
    st.metric(
        "Clinics",
        clinics_processed
    )

# --------------------
# Donut Chart
# --------------------

chart_data = pd.DataFrame({
    "Category": ["Normal", "Abnormal"],
    "Count": [normal_cases, abnormal_cases]
})

fig = px.pie(
    chart_data,
    names="Category",
    values="Count",
    hole=0.5,
    title="Normal vs Abnormal Cases"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# --------------------
# Disease Distribution
# --------------------

st.subheader("Disease Distribution")

fig2 = px.bar(
    disease_summary,
    x="Disease",
    y="Count",
    title="Disease Distribution"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

# --------------------
# Clinic-wise Volume
# --------------------

st.subheader("Clinic-wise Volume")

fig3 = px.bar(
    customer_summary,
    x="cust_id",
    y="Studies",
    title="Studies by Customer"
)

st.plotly_chart(
    fig3,
    use_container_width=True
)

# --------------------
# Daily Trend
# --------------------

st.subheader("Daily Trend")

fig4 = px.line(
    daily_trend,
    x="date",
    y="Studies",
    markers=True,
    title="Daily X-Ray Volume"
)

st.plotly_chart(
    fig4,
    use_container_width=True
)

# --------------------
# Clinic Statistics
# --------------------

st.subheader("Clinic Statistics")

st.dataframe(
    clinic_summary,
    use_container_width=True
)