from fastapi import APIRouter
from fastapi.responses import FileResponse
import pandas as pd
from database.connection import load_csv
from utils.pdf_generator import generate_pdf
from utils.date_parser import parse_date 
from utils.date_ranges import last_7_days, last_30_days

router = APIRouter(prefix="/report", tags=["Sensor Overview"])

@router.get("/sensor-overview")
def get_sensor_overview(start: str, end: str):
    df = load_csv("sensor_status_overview.csv")

    df["last_updated"] = pd.to_datetime(df["last_updated"])
    start_dt = parse_date(start, True)
    end_dt = parse_date(end, False)

    filtered = df[(df["last_updated"] >= start_dt) & (df["last_updated"] <= end_dt)]

    return filtered.to_dict(orient="records")

@router.get("/sensor-overview/pdf")
def get_sensor_overview_pdf(start: str, end: str):
    df = load_csv("sensor_status_overview.csv")

    df["last_updated"] = pd.to_datetime(df["last_updated"])
    start_dt = parse_date(start, True)
    end_dt = parse_date(end, False)

    filtered = df[(df["last_updated"] >= start_dt) & (df["last_updated"] <= end_dt)]

    total_sensors = len(filtered)
    total_on = len(filtered[filtered["status"] == "ON"])
    total_off = len(filtered[filtered["status"] == "OFF"])

    summary_text = (
        f"Total Sensors: {total_sensors}\n"
        f"ON: {total_on}\n"
        f"OFF: {total_off}"
    )


    filepath = generate_pdf(
        title="Sensor Status Overview",
        start_date=start,
        end_date=end,
        df=filtered,
        output_filename="sensor_overview_report.pdf",
        summary_text=summary_text,
    )

    return FileResponse(filepath, media_type="application/pdf", filename="sensor_overview_report.pdf")

# LAST 7 DAYS
@router.get("/sensor-overview/last7")
def get_sensor_overview_last7():
    df = load_csv("sensor_status_overview.csv")
    df["last_updated"] = pd.to_datetime(df["last_updated"])

    start, end = last_7_days()

    filtered = df[(df["last_updated"] >= start) & (df["last_updated"] <= end)]
    return filtered.to_dict(orient="records")


@router.get("/sensor-overview/last7/pdf")
def get_sensor_overview_last7_pdf():
    df = load_csv("sensor_status_overview.csv")
    df["last_updated"] = pd.to_datetime(df["last_updated"])

    start, end = last_7_days()

    filtered = df[(df["last_updated"] >= start) & (df["last_updated"] <= end)]

    total_sensors = len(filtered)
    total_on = len(filtered[filtered["status"] == "ON"])
    total_off = len(filtered[filtered["status"] == "OFF"])

    summary_text = (
        f"Total Sensors: {total_sensors}\n"
        f"ON: {total_on}\n"
        f"OFF: {total_off}"
    )

    filepath = generate_pdf(
        title="Sensor Overview Report (Last 7 Days)",
        start_date=start.strftime("%Y-%m-%d"),
        end_date=end.strftime("%Y-%m-%d"),
        df=filtered,
        output_filename="sensor_overview_last7.pdf",
        summary_text=summary_text,
    )

    return FileResponse(filepath, media_type="application/pdf", filename="sensor_overview_last7.pdf")


# LAST 30 DAYS 
@router.get("/sensor-overview/last30")
def get_sensor_overview_last30():
    df = load_csv("sensor_status_overview.csv")
    df["last_updated"] = pd.to_datetime(df["last_updated"])

    start, end = last_30_days()

    filtered = df[(df["last_updated"] >= start) & (df["last_updated"] <= end)]
    return filtered.to_dict(orient="records")


@router.get("/sensor-overview/last30/pdf")
def get_sensor_overview_last30_pdf():
    df = load_csv("sensor_status_overview.csv")
    df["last_updated"] = pd.to_datetime(df["last_updated"])

    start, end = last_30_days()

    filtered = df[(df["last_updated"] >= start) & (df["last_updated"] <= end)]

    total_sensors = len(filtered)
    total_on = len(filtered[filtered["status"] == "ON"])
    total_off = len(filtered[filtered["status"] == "OFF"])

    summary_text = (
        f"Total Sensors: {total_sensors}\n"
        f"ON: {total_on}\n"
        f"OFF: {total_off}"
    )

    filepath = generate_pdf(
        title="Sensor Overview Report (Last 30 Days)",
        start_date=start.strftime("%Y-%m-%d"),
        end_date=end.strftime("%Y-%m-%d"),
        df=filtered,
        output_filename="sensor_overview_last30.pdf",
        summary_text=summary_text,
    )

    return FileResponse(filepath, media_type="application/pdf", filename="sensor_overview_last30.pdf")