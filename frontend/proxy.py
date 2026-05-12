from typing import Any
import os
import requests
from fastapi import FastAPI, Request, Response

API_URL = os.getenv("API_URL", "http://api:8080")

app = FastAPI(title="Frontend Proxy")


@app.get("/health")
def health():
    try:
        r = requests.get(f"{API_URL}/health", timeout=5)
        return Response(content=r.content, status_code=r.status_code, media_type=r.headers.get("Content-Type", "application/json"))
    except Exception as e:
        return {"status": "error", "error": str(e)}


@app.get("/api/nodes")
def get_nodes():
    try:
        r = requests.get(f"{API_URL}/api/nodes", timeout=5)
        return Response(content=r.content, status_code=r.status_code, media_type=r.headers.get("Content-Type", "application/json"))
    except Exception as e:
        return {"status": "error", "error": str(e)}


@app.post("/api/nodes")
async def post_node(request: Request):
    try:
        payload = await request.body()
        r = requests.post(f"{API_URL}/api/nodes", data=payload, headers={"Content-Type": "application/json"}, timeout=5)
        return Response(content=r.content, status_code=r.status_code, media_type=r.headers.get("Content-Type", "application/json"))
    except Exception as e:
        return {"status": "error", "error": str(e)}


@app.delete("/api/nodes/{name}")
def delete_node(name: str):
    try:
        r = requests.delete(f"{API_URL}/api/nodes/{name}", timeout=5)
        return Response(content=r.content, status_code=r.status_code, media_type=r.headers.get("Content-Type", "application/json"))
    except Exception as e:
        return {"status": "error", "error": str(e)}
