from fastapi import APIRouter
from fastapi.responses import FileResponse
from database.connection import load_csv
from utils.pdf_generator import generate_pdf
import pandas as pd
from utils.date_parser import parse_date

router = APIRouter(prefix="/report", tags=["Energy Generated"])


@router.get("/report/energy-generated")
def get_energy_generated(start: str, end:str):
    df = load_csv("energy_generated.csv")

    df["ts"] = pd.to_datetime(df["ts"])
    start_dt = parse_date(start, True)
    end_dt = parse_date(end, False)

    filtered = df[(df["ts"] >= start_dt) & (df["ts"] <= end_dt)]
    return filtered.to_dict(orient="records")

@router.get("/energy-generated")
def get_energy_generated_pdf(start: str, end: str):
    df = load_csv("energy_generated.csv")

    df["ts"] = pd.to_datetime(df["ts"])
    start_dt = parse_date(start, True)
    end_dt = parse_date(end, False)

    filtered = df[(df["ts"] >= start_dt) & (df["ts"] <= end_dt)]

    filepath = generate_pdf(
        title="Energy Generated Report",
        start_date=start,
        end_date=end,
        df=filtered,
        output_filename="energy_generated_report.pdf"
    )

    return FileResponse(filepath, media_type="application/pdf", filename="energy_generated_report.pdf")