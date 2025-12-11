from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import random

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "healthy", "service": "ai-signals"}

@app.get("/predict/{symbol}")
def predict(symbol: str):
    confidence = round(random.uniform(0.6, 0.95), 2)
    return {
        "symbol": symbol,
        "prediction": "BUY" if random.random() > 0.4 else "SELL",
        "confidence": confidence,
        "model": "LSTM_v1.2"
    }
