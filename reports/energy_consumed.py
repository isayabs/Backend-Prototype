from fastapi import APIRouter
from fastapi.responses import FileResponse
from database.connection import load_csv
from utils.pdf_generator import generate_pdf
import pandas as pd
from utils.date_parser import parse_date
from utils.date_ranges import last_7_days, last_30_days
from utils.grouping import group_by_date

router = APIRouter(prefix="/report", tags=["Energy Consumed"])


@router.get("/report/energy-consumed")
def energy_consumed(start: str, end: str): 
    df = load_csv("energy_consumed.csv")

    df.columns = ["sequence_number", "timestamp", "energy_consumed (kWh)"]
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    start_dt = parse_date(start, True)
    end_dt = parse_date(end, False)

    filtered = df[(df["timestamp"] >= start_dt) & (df["timestamp"] <= end_dt)]
    return filtered.to_dict(orient="records")

@router.get("/energy-consumed/pdf")
def get_energy_consumed_pdf(start: str, end: str):
    df = load_csv("energy_consumed.csv")

    df.columns = ["sequence_number", "timestamp", "energy_consumed (kWh)"]
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    start_dt = parse_date(start, True)
    end_dt = parse_date(end, False)

    filtered = df[(df["timestamp"] >= start_dt) & (df["timestamp"] <= end_dt)]
    grouped = group_by_date(filtered, "timestamp")

    filepath = generate_pdf(
        title="Energy Consumed Report",
        start_date=start,
        end_date=end,
        df=None,
        output_filename="energy_consumed_report.pdf",
        grouped_by_date=grouped
    )

    return FileResponse(filepath, media_type="application/pdf", filename="energy_consumed_report.pdf")

# LAST 7 DAYS
@router.get("/energy-consumed/last7")
def get_energy_consumed_last7():
    df = load_csv("energy_consumed.csv")

    df.columns = ["sequence_number", "timestamp", "energy_consumed (kWh)"]
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    start, end = last_7_days()

    filtered = df[(df["timestamp"] >= start) & (df["timestamp"] <= end)]
    return filtered.to_dict(orient="records")


@router.get("/energy-consumed/last7/pdf")
def get_energy_consumed_last7_pdf():
    df = load_csv("energy_consumed.csv")

    df.columns = ["sequence_number", "timestamp", "energy_consumed (kWh)"]
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    start, end = last_7_days()

    filtered = df[(df["timestamp"] >= start) & (df["timestamp"] <= end)]
    grouped = group_by_date(filtered, "timestamp")

    filepath = generate_pdf(
        title="Energy Consumed Report (Last 7 Days)",
        start_date=start.strftime("%Y-%m-%d"),
        end_date=end.strftime("%Y-%m-%d"),
        df=None,
        output_filename="energy_consumed_last7.pdf",
        grouped_by_date=grouped
    )

    return FileResponse(filepath, media_type="application/pdf", filename="energy_consumed_last7.pdf")


# LAST 30 DAYS
@router.get("/energy-consumed/last30")
def get_energy_consumed_last30():
    df = load_csv("energy_consumed.csv")

    df.columns = ["sequence_number", "timestamp", "energy_consumed (kWh)"]
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    start, end = last_30_days()

    filtered = df[(df["timestamp"] >= start) & (df["timestamp"] <= end)]
    return filtered.to_dict(orient="records")


@router.get("/energy-consumed/last30/pdf")
def get_energy_consumed_last30_pdf():
    df = load_csv("energy_consumed.csv")

    df.columns = ["sequence_number", "timestamp", "energy_consumed (kWh)"]
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    start, end = last_30_days()

    filtered = df[(df["timestamp"] >= start) & (df["timestamp"] <= end)]
    grouped = group_by_date(filtered, "timestamp")

    filepath = generate_pdf(
        title="Energy Consumed Report (Last 30 Days)",
        start_date=start.strftime("%Y-%m-%d"),
        end_date=end.strftime("%Y-%m-%d"),
        df=None,
        output_filename="energy_consumed_last30.pdf",
        grouped_by_date=grouped
    )

    return FileResponse(filepath, media_type="application/pdf", filename="energy_consumed_last30.pdf")
