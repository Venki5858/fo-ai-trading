from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import time

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Order(BaseModel):
    symbol: str
    side: str
    quantity: int
    price: float

orders = []

@app.get("/health")
def health():
    return {"status": "healthy", "service": "order-engine"}

@app.post("/execute")
def execute_order(order: Order):
    order_id = f"ORD-{int(time.time())}"
    orders.append({"id": order_id, **order.dict()})
    return {"order_id": order_id, "status": "EXECUTED", "timestamp": time.time()}
