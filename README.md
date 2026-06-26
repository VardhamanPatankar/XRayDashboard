# X-Ray Analytics Dashboard

## Project Overview

The **X-Ray Analytics Dashboard** is an interactive data analytics application built using **Python** and **Streamlit**.

It processes AI-generated X-ray prediction logs from clinics and diagnostic centers, providing real-time operational insights through interactive visualizations, KPI cards, filters, and downloadable reports.

The dashboard automatically refreshes every minute and reads data from a single Excel file, allowing clinics to continuously update the same file without uploading a new one each day.

## Features

### KPI Metrics

- Total X-Rays Processed
- Normal Cases
- Abnormal Cases
- Abnormality Percentage
- Active Clinics

### Dashboard Visualizations

- Normal vs Abnormal Cases (Donut Chart)
- Disease Distribution (Bar Chart)
- Clinic-wise Volume (Bar Chart)
- Daily X-Ray Volume (Line Chart)
- Daily Normal vs Abnormal Trend (Dual Line Chart)

### Interactive Filters

- Date Range
- Clinic
- Image Category
- Prediction Outcome

## Live Dashboard Updates

- Reads data directly from a single Excel file
- Auto-refreshes every 1 minute
- Displays:
  - Last Dashboard Refresh Time
  - Last Excel File Updated Time

## Downloadable Reports

Generate reports directly from the dashboard:

- CSV Report
- Excel Report
- PDF Report

## Technologies Used

- Python
- Streamlit
- Pandas
- Plotly Express
- OpenPyXL
- ReportLab
- streamlit-autorefresh
- Git
- GitHub

## Project Structure

```text
XRayDashboard/

├── dashboard/
│   └── app.py

├── data/
│   └── prediction_logs.xlsx

├── scripts/
│   ├── read_data.py
│   ├── validate_data.py
│   ├── kpi.py
│   ├── disease_summary.py
│   ├── clinic_summary.py
│   ├── generate_report.py
│   └── temporary.py

├── .gitignore

├── requirements.txt

└── README.md
```

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/VardhamanPatankar/XRayDashboard.git
```

### 2. Move into the project

```bash
cd XRayDashboard
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the virtual environment

**Windows**

```bash
venv\Scripts\activate
```

### 5. Install dependencies

```bash
pip install pandas streamlit plotly openpyxl reportlab streamlit-autorefresh
```

## Run the Dashboard

```bash
streamlit run dashboard/app.py
```

The dashboard will be available at:

```text
http://localhost:8501
```

## Dashboard Highlights

✔ Interactive KPI Cards

✔ Dynamic Filtering

✔ Live Excel Integration

✔ Auto Refresh

✔ Disease Classification

✔ Clinic Statistics

✔ Daily Trend Analysis

✔ Downloadable Reports (CSV, Excel & PDF)

✔ Responsive Dashboard Layout

## Future Enhancements

- Windows Task Scheduler integration
- Email notifications with daily reports
- User authentication
- Cloud deployment (Streamlit Community Cloud / Azure)
- Database integration (SQL Server/PostgreSQL)
- Additional disease analytics and visualizations

## Author
Vardhaman Patankar
