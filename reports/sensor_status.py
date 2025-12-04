from fastapi import APIRouter
from fastapi.responses import FileResponse
import pandas as pd
from database.connection import load_csv
from utils.pdf_generator import generate_pdf
from utils.date_parser import parse_date 
from utils.date_ranges import last_7_days, last_30_days

router = APIRouter(prefix="/report", tags=["Sensor Status"])

def group_latest_per_day(df):
    df["date"] = df["last_updated"].dt.date

    grouped = {}

    for date_value, df_day in df.groupby("date"):
        latest = (
            df_day.sort_values("last_updated")
                  .groupby("sensor_id")
                  .tail(1)
                  .sort_values("last_updated", ascending=False)
        )
        grouped[date_value] = latest

    return grouped

@router.get("/sensor-status")
def get_sensor_status(start: str, end: str):
    df = load_csv("sensor_status.csv")
    df["last_updated"] = pd.to_datetime(df["last_updated"])

    start_dt = parse_date(start, True)
    end_dt = parse_date(end, False)

    filtered = df[(df["last_updated"] >= start_dt) & (df["last_updated"] <= end_dt)]
    grouped = group_latest_per_day(filtered)

    return {str(date): grouped[date].to_dict(orient="records") for date in grouped}

@router.get("/sensor-status/pdf")
def get_sensor_status_pdf(start: str, end: str):
    df = load_csv("sensor_status.csv")

    df["last_updated"] = pd.to_datetime(df["last_updated"])
    start_dt = parse_date(start, True)
    end_dt = parse_date(end, False)

    filtered = df[(df["last_updated"] >= start_dt) & (df["last_updated"] <= end_dt)]
    grouped = group_latest_per_day(filtered)

    combined = pd.concat(grouped.values(), ignore_index=True)

    summary_text = (
        f"Total Sensors: {len(combined)}\n"
        f"ON: {combined['status'].eq('ON').sum()}\n"
        f"OFF: {combined['status'].eq('OFF').sum()}"
    )

    filepath = generate_pdf(
        title="Sensor Status Report",
        start_date=start,
        end_date=end,
        df=None,                      
        grouped_by_date=grouped,      
        output_filename="sensor_status_report.pdf",
        summary_text=summary_text,
    )

    return FileResponse(filepath, media_type="application/pdf", filename="sensor_status_report.pdf")

# LAST 7 DAYS
@router.get("/sensor-status/last7")
def get_sensor_status_last7():
    df = load_csv("sensor_status.csv")
    df["last_updated"] = pd.to_datetime(df["last_updated"])

    start, end = last_7_days()
    filtered = df[(df["last_updated"] >= start) & (df["last_updated"] <= end)]
    grouped = group_latest_per_day(filtered)

    return {str(date): grouped[date].to_dict(orient="records") for date in grouped}

@router.get("/sensor-status/last7/pdf")
def get_sensor_status_last7_pdf():
    df = load_csv("sensor_status.csv")
    df["last_updated"] = pd.to_datetime(df["last_updated"])

    start, end = last_7_days()
    filtered = df[(df["last_updated"] >= start) & (df["last_updated"] <= end)]
    grouped = group_latest_per_day(filtered)

    combined = pd.concat(grouped.values(), ignore_index=True)

    summary_text = (
        f"Total Sensors: {len(combined)}\n"
        f"ON: {combined['status'].eq('ON').sum()}\n"
        f"OFF: {combined['status'].eq('OFF').sum()}"
    )

    filepath = generate_pdf(
        title="Sensor Status Report (Last 7 Days)",
        start_date=start.strftime("%Y-%m-%d"),
        end_date=end.strftime("%Y-%m-%d"),
        df=None,
        grouped_by_date=grouped,
        output_filename="sensor_status_last7.pdf",
        summary_text=summary_text,
    )

    return FileResponse(filepath, media_type="application/pdf", filename="sensor_status_last7.pdf")


# LAST 30 DAYS 
@router.get("/sensor-status/last30")
def get_sensor_status_last30():
    df = load_csv("sensor_status.csv")
    df["last_updated"] = pd.to_datetime(df["last_updated"])

    start, end = last_30_days()
    filtered = df[(df["last_updated"] >= start) & (df["last_updated"] <= end)]
    grouped = group_latest_per_day(filtered)

    return {str(date): grouped[date].to_dict(orient="records") for date in grouped}


@router.get("/sensor-status/last30/pdf")
def get_sensor_status_last30_pdf():
    df = load_csv("sensor_status.csv")
    df["last_updated"] = pd.to_datetime(df["last_updated"])

    start, end = last_30_days()
    filtered = df[(df["last_updated"] >= start) & (df["last_updated"] <= end)]
    grouped = group_latest_per_day(filtered)

    combined = pd.concat(grouped.values(), ignore_index=True)

    summary_text = (
        f"Total Sensors: {len(combined)}\n"
        f"ON: {combined['status'].eq('ON').sum()}\n"
        f"OFF: {combined['status'].eq('OFF').sum()}"
    )

    filepath = generate_pdf(
        title="Sensor Status Report (Last 30 Days)",
        start_date=start.strftime("%Y-%m-%d"),
        end_date=end.strftime("%Y-%m-%d"),
        df=None,
        grouped_by_date=grouped,
        output_filename="sensor_status_last30.pdf",
        summary_text=summary_text,
    )
    return FileResponse(filepath, media_type="application/pdf", filename="sensor_status_last30.pdf")