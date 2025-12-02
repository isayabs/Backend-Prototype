from fastapi import APIRouter 
from database.connection import load_csv

router = APIRouter()

@router.get("/report/sensor-status")
def get_sensor_status():
    df = load_csv("sensor_status.csv")
    return df.to_dict(orient="records")