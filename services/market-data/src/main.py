from fastapi import FastAPI
import datetime as dt

app = FastAPI(title="Market Data")

@app.get("/nifty")
def nifty():
    return {
        "symbol": "NIFTY",
        "price": 25870,
        "open": 25700,
        "high": 25950,
        "low": 25600,
        "close": 25800,
        "datetime": dt.datetime.utcnow().isoformat()
    }

@app.get("/banknifty")
def banknifty():
    return {
        "symbol": "BANKNIFTY",
        "price": 55000,
        "open": 54800,
        "high": 55200,
        "low": 54600,
        "close": 54950,
        "datetime": dt.datetime.utcnow().isoformat()
    }
