from fastapi import APIRouter
from fastapi.responses import FileResponse
from database.connection import load_csv
from utils.pdf_generator import generate_pdf 
from datetime import datetime
import pandas as pd

router = APIRouter()


@router.get("/report/temperature")
def temperature(start: str, end: str):
    df = load_csv("temperature.csv")
    df["ts"] = pd.to_datetime(df["ts"])

    start_dt = datetime.fromisoformat(start)
    end_dt = datetime.fromisoformat(end)

    filtered = df[(df["ts"] >= start_dt) & (df["ts"] <= end_dt)]
    return filtered.to_dict(orient="records")

@router.get("/report/temperature/pdf")
def temperature_pdf(start: str, end: str):
    df = load_csv("temperature.csv")
    df["ts"] = pd.to_datetime(df["ts"])

    start_dt = datetime.fromisoformat(start)
    end_dt = datetime.fromisoformat(end)

    filtered = df[(df["ts"] >= start_dt) & (df["ts"] <= end_dt)]

    file_path = generate_pdf("Temperature Report", filtered, "temperature_report.pdf")
    return FileResponse(file_path, media_type="application/pdf")