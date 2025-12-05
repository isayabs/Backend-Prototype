from fastapi import APIRouter
from fastapi.responses import FileResponse
from database.connection import load_csv
from utils.pdf_generator import generate_pdf
import pandas as pd
from utils.date_parser import parse_date
from utils.date_ranges import last_7_days, last_30_days
from utils.grouping import group_by_date

router = APIRouter(prefix="/report", tags=["Energy Generated"])


@router.get("/energy-generated")
def get_energy_generated(start: str, end:str):
    df = load_csv("energy_generated.csv")

    df.columns = ["sequence_number", "timestamp", "energy_generated (kWh)"]
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    start_dt = parse_date(start, True)
    end_dt = parse_date(end, False)

    filtered = df[(df["timestamp"] >= start_dt) & (df["timestamp"] <= end_dt)]
    return filtered.to_dict(orient="records")

@router.get("/energy-generated/pdf")
def get_energy_generated_pdf(start: str, end: str):
    df = load_csv("energy_generated.csv")

    df.columns = ["sequence_number", "timestamp", "energy_generated (kWh)"]
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    start_dt = parse_date(start, True)
    end_dt = parse_date(end, False)

    filtered = df[(df["timestamp"] >= start_dt) & (df["timestamp"] <= end_dt)]
    grouped = group_by_date(filtered, "timestamp")

    filepath = generate_pdf(
        title="Energy Generated Report",
        start_date=start,
        end_date=end,
        df=None,
        output_filename="energy_generated_report.pdf",
        grouped_by_date=grouped
    )

    return FileResponse(filepath, media_type="application/pdf", filename="energy_generated_report.pdf")

# LAST 7 DAYS
@router.get("/energy-generated/last7")
def get_energy_generated_last7():
    df = load_csv("energy_generated.csv")

    df.columns = ["sequence_number", "timestamp", "energy_generated (kWh)"]
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    start, end = last_7_days()

    filtered = df[(df["timestamp"] >= start) & (df["timestamp"] <= end)]
    return filtered.to_dict(orient="records")


@router.get("/energy-generated/last7/pdf")
def get_energy_generated_last7_pdf():
    df = load_csv("energy_generated.csv")

    df.columns = ["sequence_number", "timestamp", "energy_generated (kWh)"]
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    start, end = last_7_days()

    filtered = df[(df["timestamp"] >= start) & (df["timestamp"] <= end)]
    grouped = group_by_date(filtered, "timestamp")

    filepath = generate_pdf(
        title="Energy Generated Report (Last 7 Days)",
        start_date=start.strftime("%Y-%m-%d"),
        end_date=end.strftime("%Y-%m-%d"),
        df=None,
        output_filename="energy_generated_last7.pdf",
        grouped_by_date=grouped
    )

    return FileResponse(filepath, media_type="application/pdf", filename="energy_generated_last7.pdf")


# LAST 30 DAYS
@router.get("/energy-generated/last30")
def get_energy_generated_last30():
    df = load_csv("energy_generated.csv")

    df.columns = ["sequence_number", "timestamp", "energy_generated (kWh)"]
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    start, end = last_30_days()

    filtered = df[(df["timestamp"] >= start) & (df["timestamp"] <= end)]
    return filtered.to_dict(orient="records")


@router.get("/energy-generated/last30/pdf")
def get_energy_generated_last30_pdf():
    df = load_csv("energy_generated.csv")

    df.columns = ["sequence_number", "timestamp", "energy_generated (kWh)"]
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    start, end = last_30_days()

    filtered = df[(df["timestamp"] >= start) & (df["timestamp"] <= end)]
    grouped = group_by_date(filtered, "timestamp")

    filepath = generate_pdf(
        title="Energy Generated Report (Last 30 Days)",
        start_date=start.strftime("%Y-%m-%d"),
        end_date=end.strftime("%Y-%m-%d"),
        df=None,
        output_filename="energy_generated_last30.pdf",
        grouped_by_date=grouped
    )

    return FileResponse(filepath, media_type="application/pdf", filename="energy_generated_last30.pdf")