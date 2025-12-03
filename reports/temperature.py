from fastapi import APIRouter
from fastapi.responses import FileResponse
from database.connection import load_csv
from utils.pdf_generator import generate_pdf 
import pandas as pd
from utils.date_parser import parse_date
from utils.date_ranges import last_7_days, last_30_days

router = APIRouter(prefix="/report", tags=["Temperature"])


@router.get("/temperature")
def get_temperature(start: str, end: str):
    df = load_csv("temperature.csv")

    df["ts"] = pd.to_datetime(df["ts"])
    start_dt = parse_date(start, True)
    end_dt = parse_date(end, False)

    filtered = df[(df["ts"] >= start_dt) & (df["ts"] <= end_dt)]
    return filtered.to_dict(orient="records")

@router.get("/temperature/pdf")
def get_temperature_pdf(start: str, end: str):
    df = load_csv("temperature.csv")

    df["ts"] = pd.to_datetime(df["ts"])
    start_dt = parse_date(start, True)
    end_dt = parse_date(end, False)

    filtered = df[(df["ts"] >= start_dt) & (df["ts"] <= end_dt)]

    filepath = generate_pdf(
        title="Temperature Inside the Building Report",
        start_date=start,
        end_date=end,
        df=filtered,
        output_filename="temperature_report.pdf"
    )

    return FileResponse(filepath, media_type="application/pdf", filename="temperature_report.pdf")

# LAST 7 DAYS
@router.get("/temperature/last7")
def get_temperature_last7():
    df = load_csv("temperature.csv")
    df["ts"] = pd.to_datetime(df["ts"])

    start, end = last_7_days()

    filtered = df[(df["ts"] >= start) & (df["ts"] <= end)]
    return filtered.to_dict(orient="records")


@router.get("/temperature/last7/pdf")
def get_temperature_last7_pdf():
    df = load_csv("temperature.csv")
    df["ts"] = pd.to_datetime(df["ts"])

    start, end = last_7_days()

    filtered = df[(df["ts"] >= start) & (df["ts"] <= end)]

    filepath = generate_pdf(
        title="Temperature Report (Last 7 Days)",
        start_date=start.strftime("%Y-%m-%d"),
        end_date=end.strftime("%Y-%m-%d"),
        df=filtered,
        output_filename="temperature_report_last7.pdf"
    )

    return FileResponse(filepath, media_type="application/pdf", filename="temperature_report_last7.pdf")

# LAST 30 DAYS 
@router.get("/temperature/last30")
def get_temperature_last30():
    df = load_csv("temperature.csv")
    df["ts"] = pd.to_datetime(df["ts"])

    start, end = last_30_days()

    filtered = df[(df["ts"] >= start) & (df["ts"] <= end)]
    return filtered.to_dict(orient="records")


@router.get("/temperature/last30/pdf")
def get_temperature_last30_pdf():
    df = load_csv("temperature.csv")
    df["ts"] = pd.to_datetime(df["ts"])

    start, end = last_30_days()

    filtered = df[(df["ts"] >= start) & (df["ts"] <= end)]

    filepath = generate_pdf(
        title="Temperature Report (Last 30 Days)",
        start_date=start.strftime("%Y-%m-%d"),
        end_date=end.strftime("%Y-%m-%d"),
        df=filtered,
        output_filename="temperature_report_last30.pdf"
    )

    return FileResponse(filepath, media_type="application/pdf", filename="temperature_report_last30.pdf")