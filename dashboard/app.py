import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_autorefresh import st_autorefresh
from datetime import datetime
import os
from io import BytesIO
from openpyxl import Workbook
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors

st.set_page_config(
    page_title="X-Ray Analytics Dashboard",
    page_icon="🩻",
    layout="wide"
)

# --------------------
# Auto Refresh
# --------------------

st_autorefresh(
    interval=60000,  # 1 minute
    key="dashboard_refresh"
)

# --------------------
# Load Data
# --------------------

excel_file = "data/prediction_logs.xlsx"
df = pd.read_excel(excel_file)

excel_last_updated = datetime.fromtimestamp(
    os.path.getmtime(excel_file)
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

st.sidebar.header("🔍Filters")
st.sidebar.caption(
    "Use the filters below to explore the dashboard."
)
# --------------------
# Date Filter
# --------------------

start_date = st.sidebar.date_input(
    "Start Date",
    value=df["date"].min()
)

end_date = st.sidebar.date_input(
    "End Date",
    value=df["date"].max()
)

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

# --------------------
# Apply Filters
# --------------------

filtered_df = df[
    (df["date"] >= start_date)
    &
    (df["date"] <= end_date)
    &
    (df["cust_id"].isin(customers))
    &
    (df["image_category"].isin(image_categories))
    &
    (df["flag_abnormal"].isin(outcomes))
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
clinic_summary["abnormal_pct"] = (
    clinic_summary["abnormal_pct"]
    .round(2)
)

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

def generate_excel(dataframe):

    wb = Workbook()
    ws = wb.active
    ws.title = "Clinic Summary"

    ws.append(list(dataframe.columns))

    for row in dataframe.itertuples(index=False):
        ws.append(list(row))

    excel_file = BytesIO()
    wb.save(excel_file)
    excel_file.seek(0)

    return excel_file

def generate_pdf(dataframe):

    buffer = BytesIO()

    pdf = SimpleDocTemplate(buffer)

    data = [list(dataframe.columns)]

    for row in dataframe.itertuples(index=False):
        data.append(list(row))

    table = Table(data)

    table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
            ("GRID", (0, 0), (-1, -1), 1, colors.black),
            ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ])
    )

    pdf.build([table])

    buffer.seek(0)

    return buffer

# --------------------
# Dashboard Title
# --------------------

st.title("🩻X-Ray Analytics Dashboard")
st.caption(
    f"🟢 Last Refreshed: {datetime.now().strftime('%d/%m/%Y %I:%M:%S %p')}"
)
st.caption(
    f"📄 Excel Last Updated: {excel_last_updated.strftime('%d/%m/%Y %I:%M:%S %p')}"
)

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

st.divider()

# --------------------
# Charts Row 1
# --------------------

left_col, right_col = st.columns(2)

with left_col:

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

with right_col:

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
# Daily Trend
# --------------------
st.header("Daily Trends")

left_col, right_col = st.columns(2)

with left_col:

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

with right_col:

    daily_status = (
        filtered_df
        .groupby(["date", "flag_abnormal"])
        .size()
        .reset_index(name="Studies")
    )

    daily_status["flag_abnormal"] = (
        daily_status["flag_abnormal"]
        .replace({
            "no": "Normal",
            "yes": "Abnormal"
        })
    )

    fig5 = px.line(
        daily_status,
        x="date",
        y="Studies",
        color="flag_abnormal",
        markers=True,
        title="Daily Normal vs Abnormal Cases"
    )

    fig5.update_layout(
        legend_title="Case Type"
    )

    st.plotly_chart(
        fig5,
        use_container_width=True
    )

st.divider()

# --------------------
# Clinic Statistics
# --------------------
clinic_summary["abnormal_pct"] = (
    clinic_summary["abnormal_pct"]
    .round(2)
)

st.subheader("Clinic Statistics")

st.dataframe(
    clinic_summary,
    use_container_width=True
)

# --------------------
# Report Data
# --------------------
st.divider()
st.subheader("📄 Reports")

report_df = clinic_summary.copy()

# --------------------
# Download CSV Report
# --------------------

csv = report_df.to_csv(index=False).encode("utf-8")
excel_data = generate_excel(report_df)
pdf_data = generate_pdf(report_df)

st.download_button(
    label="📥 Download CSV Report",
    data=csv,
    file_name="clinic_summary.csv",
    mime="text/csv"
)

st.download_button(
    label="📥 Download Excel Report",
    data=excel_data,
    file_name="clinic_summary.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

st.download_button(
    label="📄 Download PDF Report",
    data=pdf_data,
    file_name="clinic_summary.pdf",
    mime="application/pdf"
)

# --------------------
# Image Explorer
# --------------------

st.divider()

st.header("🔎 Image Explorer")

selected_image = st.selectbox(
    "Select Image",
    options=sorted(df["image_name"].unique())
)

selected_row = df[
    df["image_name"] == selected_image
].iloc[0]

# --------------------
# Image Details
# --------------------

st.subheader("Image Details")

col1, col2 = st.columns(2)

with col1:
    st.write(f"**Image Name:** {selected_row['image_name']}")
    patient_id = selected_row["patient_id"]
    if pd.isna(patient_id):
        patient_id = "N/A"
    st.write(f"**Patient ID:** {patient_id}")
    st.write(f"**Clinic:** {selected_row['cust_id']}")
    st.write(f"**Category:** {selected_row['image_category']}")

with col2:
    st.write(f"**Outcome:** {'Abnormal' if selected_row['flag_abnormal']=='yes' else 'Normal'}")
    st.write(f"**Disease:** {classify_disease(selected_row['pred_summary'])}")
    st.write(f"**Severity:** {selected_row['severity_level']}")
    timestamp = datetime.strptime(
    selected_row["timestamp.1"],
    "%Y-%m-%d_%H:%M:%S"
    )
    st.write(
    f"**Timestamp:** {timestamp.strftime('%d %b %Y, %I:%M %p')}"
    )

st.expander("📋 Prediction Summary", expanded=False).write(
    selected_row["pred_summary"]
)