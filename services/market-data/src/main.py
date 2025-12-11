from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from pathlib import Path

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_PATH = Path("/app/data/nifty_sample.csv")

@app.get("/health")
def health():
    return {"status": "healthy", "service": "market-data"}

@app.get("/nifty")
def get_nifty():
    if not DATA_PATH.exists():
        return {"error": "CSV not found", "path": str(DATA_PATH)}
    df = pd.read_csv(DATA_PATH)
    last = df.tail(1).iloc[0]
    return {
        "symbol": "NIFTY",
        "datetime": str(last["datetime"]),
        "price": float(last["close"]),
        "open": float(last["open"]),
        "high": float(last["high"]),
        "low": float(last["low"]),
        "close": float(last["close"])
    }
