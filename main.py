from fastapi import FastAPI
from reports.temperature import router as temp_router
from reports.energy_generated import router as gen_rounter
from reports.energy_consumed import router as cons_router
from reports.sensor_status import router as sensor_status_router 

app = FastAPI()
app.include_router(sensor_status_router)
app.include_router(temp_router)
app.include_router(gen_rounter)
app.include_router(cons_router)

@app.get("/")
def root():
    return {"message": "Backend Prototype Running!"}