import pandas as pd
from pathlib import Path
import json

DATA_PATH = Path("data/nifty_sample.csv")
MODEL_DIR = Path("models")
MODEL_DIR.mkdir(exist_ok=True)

def train():
    if not DATA_PATH.exists():
        raise FileNotFoundError(f"CSV not found: {DATA_PATH}")
    df = pd.read_csv(DATA_PATH)
    df["sma_short"] = df["close"].rolling(window=2).mean()
    df["sma_long"] = df["close"].rolling(window=3).mean()
    last = df.tail(1).iloc[0]
    signal = "BUY" if last["sma_short"] > last["sma_long"] else "SELL"
    model = {
        "strategy": "SMA crossover",
        "short_window": 2,
        "long_window": 3,
        "last_datetime": str(last["datetime"]),
        "last_price": float(last["close"]),
        "signal": signal
    }
    with open(MODEL_DIR / "model.json", "w") as f:
        json.dump(model, f, indent=2)

if __name__ == "__main__":
    train()
