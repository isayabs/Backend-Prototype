from fastapi import APIRouter
from fastapi.responses import FileResponse
import pandas as pd 
from database.connection import load_csv
from utils.pdf_generator import generate_pdf

router = APIRouter(prefix="/report", tags=["Sensor Status"])

@router.get("/sensor-status")
def get_sensor_status(start: str, end: str):
    df = load_csv("sensor_status.csv")
    
    df["ts"] = pd.to_datetime(df["ts"])
    start_dt = pd.to_datetime(start)
    end_dt = pd.to_datetime(end)

    filtered = df[(df["ts"] >= start_dt) & (df["ts"] <= end_dt)]
    return filtered.to_dict(orient="records")

@router.get("/sensor-status/pdf")
def get_sensor_status_pdf(start: str, end: str):
    df = load_csv("sensor_status.csv")

    df["ts"] = pd.to_datetime(df["ts"])
    start_dt = pd.to_datetime(start)
    end_dt = pd.to_datetime(end)

    filtered = df[(df["ts"] >= start_dt) & (df["ts"] <= end_dt)]

    filepath = generate_pdf(
        title="Sensor Status Report",
        start_date=start,
        end_date=end,
        df=filtered,
        output_filename="sensor_status_report.pdf"
    )

    return FileResponse(filepath, media_type="application/pdf", filename="sensor_status_report.pdf")