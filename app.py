import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from src.utils.predictor import HousePricePredictor

app = FastAPI(title="LuxEstate Predictor")

# Setup for Frontend
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Predictor Instance
predictor = HousePricePredictor()

# CORS for local testing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class HouseInput(BaseModel):
    location: str
    total_sqft: float
    bath: int
    bhk: int

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("app.html", {"request": request})

@app.get("/get_location_names")
async def get_locations():
    return {"locations": predictor.columns[3:]}

@app.post("/predict")
async def predict(data: HouseInput):
    prediction = predictor.predict_price(data.location, data.total_sqft, data.bath, data.bhk)
    return {"estimated_price": prediction}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)