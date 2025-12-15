import os
import sys

from fastapi import FastAPI
import pandas as pd

# Add /app/strategies to Python path so we can import sma.py
sys.path.append("/app/strategies")
from sma import add_sma_signals  # returns columns like close, maybe signal or signal_side

app = FastAPI(title="AI Signals")

DATA_DIR = os.getenv("DATA_DIR", "/data/live")
NIFTY_CSV = os.path.join(DATA_DIR, "NIFTY_recent.csv")

FAST = int(os.getenv("SMA_FAST", "10"))
SLOW = int(os.getenv("SMA_SLOW", "20"))


def latest_sma_signal(path: str):
    if not os.path.exists(path):
        return None

    df = pd.read_csv(path)
    df["datetime"] = pd.to_datetime(df["datetime"])
    df = df.sort_values("datetime").reset_index(drop=True)

    # add strategy signals
    df = add_sma_signals(df, fast=FAST, slow=SLOW)

    last = df.iloc[-1]

    # decide signal text safely
    if "signal_side" in last:
        side = str(last["signal_side"]).upper()
    elif "signal" in last:
        val = last["signal"]
        side = "BUY" if val == 1 else "SELL" if val == -1 else "FLAT"
    else:
        side = "FLAT"

    info = {
        "price": float(last["close"]),
        "signal": side,
        "datetime": last["datetime"].isoformat(),
        "change_pct": float(last["change_pct"]) if "change_pct" in last else None,
    }
    return info


@app.get("/predict/{symbol}")
def predict(symbol: str):
    symbol = symbol.upper()

    if symbol == "NIFTY":
        info = latest_sma_signal(NIFTY_CSV)
    else:
        info = None

    if info is None:
        return {
            "symbol": symbol,
            "prediction": "UNKNOWN",
            "model": f"SMA_{FAST}_{SLOW}",
            "confidence": 0.0,
            "price": 0,
            "change_pct": None,
            "last_datetime": None,
        }

    return {
        "symbol": symbol,
        "prediction": info["signal"],
        "model": f"SMA_{FAST}_{SLOW}",
        "confidence": 0.9,
        "price": info["price"],
        "change_pct": info["change_pct"],
        "last_datetime": info["datetime"],
    }
