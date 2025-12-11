from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import httpx
import asyncio

app = FastAPI(title="F&O Trading Gateway")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "healthy", "service": "api-gateway"}

@app.get("/nifty")
async def get_nifty():
    async with httpx.AsyncClient() as client:
        resp = await client.get("http://market-data:5000/nifty")
        ai_resp = await client.get("http://ai-signals:5000/predict/NIFTY")
        return {
            **resp.json(),
            **ai_resp.json(),
            "gateway": "combined"
        }
