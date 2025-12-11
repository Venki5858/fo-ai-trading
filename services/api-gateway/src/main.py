from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import httpx
import os
import json

app = FastAPI(title="F&O Trading Gateway")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MARKET_DATA_URL = os.getenv("MARKET_DATA_URL", "http://market-data:5000")
AI_SIGNALS_URL = os.getenv("AI_SIGNALS_URL", "http://ai-signals:5000")
PAPER_BROKER_URL = os.getenv("PAPER_BROKER_URL", "http://paper-broker:5000")
EXECUTION_MODE = os.getenv("EXECUTION_MODE", "paper")

@app.get("/health")
def health():
    return {"status": "healthy", "service": "api-gateway"}

@app.get("/nifty")
async def get_nifty():
    async with httpx.AsyncClient() as client:
        m_resp = await client.get(f"{MARKET_DATA_URL}/nifty")
        a_resp = await client.get(f"{AI_SIGNALS_URL}/predict/NIFTY")
        m = m_resp.json()
        a = a_resp.json()
        return {
            "symbol": m.get("symbol", "NIFTY"),
            "price": m.get("price"),
            "open": m.get("open"),
            "high": m.get("high"),
            "low": m.get("low"),
            "close": m.get("close"),
            "datetime": m.get("datetime"),
            "prediction": a.get("prediction"),
            "model": a.get("model"),
            "confidence": a.get("confidence"),
            "last_price": a.get("last_price"),
            "last_datetime": a.get("last_datetime"),
        }

MAX_QTY_PER_ORDER = 100
ALLOWED_SYMBOLS = {"NIFTY", "BANKNIFTY"}
ALLOWED_SIDES = {"BUY", "SELL"}

class ExecuteRequest(BaseModel):
    symbol: str
    side: str
    quantity: int
    price: float

@app.post("/execute")
async def execute_order(req: ExecuteRequest):
    symbol = req.symbol.upper()
    side = req.side.upper()

    if symbol not in ALLOWED_SYMBOLS:
        return {"error": "Symbol not allowed", "symbol": symbol}

    if side not in ALLOWED_SIDES:
        return {"error": "Side not allowed", "side": side}

    if req.quantity <= 0 or req.quantity > MAX_QTY_PER_ORDER:
        return {"error": "Invalid quantity", "max_qty": MAX_QTY_PER_ORDER}

    if EXECUTION_MODE != "paper":
        return {"error": "Live mode not implemented yet", "mode": EXECUTION_MODE}

    async with httpx.AsyncClient() as client:
        resp = await client.post(f"{PAPER_BROKER_URL}/orders", json={
            "symbol": symbol,
            "side": side,
            "quantity": req.quantity,
            "price": req.price,
        })
        out = resp.json()
        out["execution_mode"] = EXECUTION_MODE
        return out

@app.get("/banknifty")
async def get_banknifty():
    async with httpx.AsyncClient() as client:
        m_resp = await client.get(f"{MARKET_DATA_URL}/banknifty")
        a_resp = await client.get(f"{AI_SIGNALS_URL}/predict/BANKNIFTY")
        m = m_resp.json()
        a = a_resp.json()
        return {
            "symbol": m.get("symbol", "BANKNIFTY"),
            "price": m.get("price"),
            "open": m.get("open"),
            "high": m.get("high"),
            "low": m.get("low"),
            "close": m.get("close"),
            "datetime": m.get("datetime"),
            "prediction": a.get("prediction"),
            "model": a.get("model"),
            "confidence": a.get("confidence"),
            "last_price": a.get("last_price"),
            "last_datetime": a.get("last_datetime"),
        }

@app.get("/journal-stats")
async def journal_stats():
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{PAPER_BROKER_URL}/stats")
        stats = resp.json()
    return stats
