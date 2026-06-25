# X-Ray Analytics Dashboard

## Project Overview

This project processes AI-generated X-ray prediction logs from clinics and diagnostic centers and generates an interactive analytics dashboard.

The dashboard provides operational insights including:

- Total X-rays processed
- Normal vs Abnormal cases
- Disease distribution
- Customer-wise volume
- Clinic statistics
- Daily trends
- Interactive filtering

## Technologies Used

- Python
- Pandas
- Streamlit
- Plotly
- OpenPyXL
- Git
- GitHub

## Project Structure

XRayDashboard/

├── dashboard/
│   └── app.py

├── data/
│   └── prediction_logs_25062026.xlsx

├── reports/
│   ├── daily_summary.csv
│   └── daily_report.xlsx

├── scripts/
│   ├── read_data.py
│   ├── validate_data.py
│   ├── kpi.py
│   ├── disease_summary.py
│   ├── clinic_summary.py
│   └── generate_report.py

└── README.md

## Features

### KPI Metrics

- Total X-Rays
- Normal Cases
- Abnormal Cases
- Abnormality Percentage
- Clinics Processed

### Dashboard Visualizations

- Normal vs Abnormal (Donut Chart)
- Disease Distribution (Bar Chart)
- Customer-wise Volume (Bar Chart)
- Daily Trend (Line Chart)
- Image Category Distribution

### Interactive Filters

- Customer / Clinic
- Image Category
- Prediction Outcome
- Date

## Installation

Create virtual environment:

```bash
python -m venv venv
```

Activate environment:

Windows:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install pandas streamlit plotly openpyxl
```

## Run Dashboard

```bash
streamlit run dashboard/app.py
```

Dashboard URL:

```text
http://localhost:8501
```

## Reports Generated

### CSV Report

```text
reports/daily_summary.csv
```

### Excel Report

```text
reports/daily_report.xlsx
```

## Future Enhancements

- Daily automated scheduler
- PDF report generation
- Email notifications
- Cloud deployment

## Author
Vardhaman Patankar
