from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from datetime import datetime
from uuid import uuid4
import csv
import os

app = FastAPI(title="Paper Broker")

JOURNAL_PATH = os.getenv("JOURNAL_PATH", "/data/trades_journal.csv")


class OrderIn(BaseModel):
    symbol: str
    side: str  # BUY or SELL
    quantity: int
    price: float


class OrderOut(OrderIn):
    id: str
    timestamp: datetime


orders: List[OrderOut] = []
positions = {}  # {"NIFTY": {"quantity": 0, "avg_price": 0.0}}


def append_journal(order: OrderOut, realized_pnl: float = 0.0, notes: str = ""):
    exists = os.path.exists(JOURNAL_PATH)
    os.makedirs(os.path.dirname(JOURNAL_PATH), exist_ok=True)
    with open(JOURNAL_PATH, "a", newline="") as f:
        writer = csv.writer(f)
        if not exists:
            writer.writerow([
                "datetime",
                "symbol",
                "side",
                "quantity",
                "price",
                "realized_pnl_after_trade",
                "notes",
            ])
        writer.writerow([
            order.timestamp.isoformat(),
            order.symbol,
            order.side,
            order.quantity,
            order.price,
            realized_pnl,
            notes,
        ])


@app.post("/orders", response_model=OrderOut)
def place_order(order: OrderIn):
    global positions
    o = OrderOut(
        id=str(uuid4()),
        symbol=order.symbol,
        side=order.side.upper(),
        quantity=order.quantity,
        price=order.price,
        timestamp=datetime.utcnow()
    )
    orders.append(o)

    pos = positions.get(o.symbol, {"quantity": 0, "avg_price": 0.0})
    qty = pos["quantity"]
    avg = pos["avg_price"]

    if o.side == "BUY":
        new_qty = qty + o.quantity
        new_avg = ((qty * avg) + (o.quantity * o.price)) / new_qty if new_qty else 0.0
    else:  # SELL
        new_qty = qty - o.quantity
        new_avg = avg if new_qty > 0 else 0.0

    positions[o.symbol] = {"quantity": new_qty, "avg_price": new_avg}

    append_journal(o, realized_pnl=0.0, notes="")
    return o


@app.get("/orders", response_model=List[OrderOut])
def list_orders():
    return orders


@app.get("/positions")
def list_positions():
    return positions


@app.get("/stats")
def stats():
    realized_pnl = 0.0
    closed_trades = 0

    for o in orders:
        if o.side == "SELL":
            buys = [b for b in orders if b.symbol == o.symbol and b.side == "BUY" and b.timestamp <= o.timestamp]
            if buys:
                avg_buy = sum(b.price * b.quantity for b in buys) / sum(b.quantity for b in buys)
                pnl = (o.price - avg_buy) * o.quantity
                realized_pnl += pnl
                closed_trades += 1

    open_positions = {sym: pos for sym, pos in positions.items() if pos["quantity"] != 0}
    return {
        "realized_pnl": realized_pnl,
        "closed_trades": closed_trades,
        "open_positions": open_positions,
    }
