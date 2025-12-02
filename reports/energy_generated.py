from fastapi import APIRouter
from database.connection import load_csv
from datetime import datetime
import pandas as pd

router = APIRouter()


@router.get("/report/energy-generated")
def energy_generated(start: str, end:str):
    df = load_csv("energy_generated.csv")
    df["ts"] = pd.to_datetime(df["ts"])

    start_dt = datetime.fromisoformat(start)
    end_dt = datetime.fromisoformat(end)

    filtered = df[(df["ts"] >= start_dt) & (df["ts"] <= end_dt)]
    return filtered.to_dict(orient="records")