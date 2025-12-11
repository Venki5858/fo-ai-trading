# fo-ai-trading – F&O AI Trading DevOps Project

## 1. Overview
Personal + professional DevOps project: AI-driven F&O trading platform for Indian markets with FastAPI microservices, React-style dashboard, Docker, GitHub Actions CI, and Kubernetes (Docker Desktop).

## 2. Architecture
- services/market-data: FastAPI, reads NIFTY OHLC from CSV, exposes /nifty.
- services/ai-signals: FastAPI, dummy AI BUY/SELL predictions.
- services/order-engine: FastAPI, mock order execution.
- services/api-gateway: FastAPI, aggregates services for the dashboard.
- services/dashboard: Node static UI, calls api-gateway.
- data/: CSV sample file for NIFTY intraday.
- k8s/: Kubernetes manifests for market-data, api-gateway, dashboard.

## 3. Local development (Docker Compose)
1. Start all services:
   docker-compose up -d --build
2. Check health:
   curl http://localhost:8000/health
3. Open dashboard:
   http://localhost:3000

## 4. GitHub Actions CI
On every push to main:
- Builds all Docker images with docker compose.
- Starts stack and checks:
  - http://localhost:8000/health
  - http://localhost:3000

## 5. Kubernetes (Docker Desktop)
1. Enable Kubernetes in Docker Desktop.
2. Apply manifests:
   kubectl apply -f services/market-data/k8s/
   kubectl apply -f services/api-gateway/k8s/
   kubectl apply -f services/dashboard/k8s/
3. Open dashboard from cluster:
   http://localhost:30000

## 6. Future work
- Replace CSV with live NSE data API.
- Add real ML model (LSTM) for F&O signals.
- Deploy to AWS EKS using Terraform and GitOps (ArgoCD).
