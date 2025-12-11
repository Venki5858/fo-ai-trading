from fastapi import FastAPI
import json
import os

app = FastAPI(title="AI Signals")

MODEL_PATH = os.getenv("MODEL_PATH", "/models/model.json")

def load_model():
    if os.path.exists(MODEL_PATH):
        with open(MODEL_PATH, "r") as f:
            return json.load(f)
    return {"model": "SMA crossover", "prediction": "BUY", "confidence": 0.9}

@app.get("/predict/{symbol}")
def predict(symbol: str):
    m = load_model()
    return {
        "symbol": symbol.upper(),
        "prediction": m.get("prediction", "BUY"),
        "model": m.get("model", "SMA crossover"),
        "confidence": m.get("confidence", 0.9),
        "last_price": m.get("last_price", 0),
        "last_datetime": m.get("last_datetime", None),
    }
