from fastapi import APIRouter
from fastapi.responses import FileResponse
from database.connection import load_csv
from utils.pdf_generator import generate_pdf 
import pandas as pd
from utils.date_parser import parse_date

router = APIRouter(prefix="/report", tags=["Temperature"])


@router.get("/report/temperature")
def get_temperature(start: str, end: str):
    df = load_csv("temperature.csv")

    df["ts"] = pd.to_datetime(df["ts"])
    start_dt = parse_date(start, True)
    end_dt = parse_date(end, False)

    filtered = df[(df["ts"] >= start_dt) & (df["ts"] <= end_dt)]
    return filtered.to_dict(orient="records")

@router.get("/report/temperature/pdf")
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