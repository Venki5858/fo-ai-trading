from fastapi import FastAPI
from pydantic import BaseModel
from kiteconnect import KiteConnect
import os

app = FastAPI(title="Live Broker (Zerodha stub)")

API_KEY = os.getenv("Z_KITE_API_KEY", "")
API_SECRET = os.getenv("Z_KITE_API_SECRET", "")
ACCESS_TOKEN = os.getenv("Z_KITE_ACCESS_TOKEN", "")

kite = None

class OrderIn(BaseModel):
    symbol: str
    side: str
    quantity: int
    price: float

@app.on_event("startup")
def init_kite():
    global kite
    if not API_KEY:
        return
    kite = KiteConnect(api_key=API_KEY)
    if ACCESS_TOKEN:
        kite.set_access_token(ACCESS_TOKEN)

@app.get("/login-url")
def login_url():
    if not API_KEY:
        return {"error": "Z_KITE_API_KEY not set"}
    k = KiteConnect(api_key=API_KEY)
    return {"login_url": k.login_url()}

@app.post("/orders")
def place_live_order(order: OrderIn):
    # SAFETY: do NOT place real orders yet
    return {
        "error": "Live broker not wired yet",
        "received": order.dict(),
        "note": "Next step will map this to kite.place_order",
    }

@app.get("/profile")
def get_profile():
    if not kite:
        return {"error": "Kite client not initialised. Check API key / access token."}
    try:
        user = kite.profile()
        return user
    except Exception as e:
        return {"error": str(e)}
    
@app.get("/margins")
def get_margins():
    if not kite:
        return {"error": "Kite client not initialised. Check tokens."}
    try:
        return kite.margins()  # equity + commodity
    except Exception as e:
        return {"error": str(e)}

