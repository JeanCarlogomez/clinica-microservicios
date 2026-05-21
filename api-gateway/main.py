from fastapi import FastAPI, APIRouter, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests
import os

app = FastAPI(title="API Gateway Clinica")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

router = APIRouter(prefix="/api/v1")

SERVICES = {
    "auth": os.getenv("AUTH_SERVICE_URL", "http://auth:8001"),
    "pacientes": os.getenv("PACIENTES_SERVICE_URL", "http://ms-pacientes:8002"),
    "citas": os.getenv("CITAS_SERVICE_URL", "http://ms-citas:8003"),
    "historial": os.getenv("HISTORIAL_SERVICE_URL", "http://ms-historial:8004"),
}


@router.get("/{service_name}/{path:path}")
async def forward_get(service_name: str, path: str, request: Request):
    if service_name not in SERVICES:
        raise HTTPException(
            status_code=404, detail=f"Service '{service_name}' not found."
        )
    service_url = f"{SERVICES[service_name]}/api/v1/{path}"
    try:
        response = requests.get(service_url, params=request.query_params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error forwarding request: {e}")


@router.post("/{service_name}/{path:path}")
async def forward_post(service_name: str, path: str, request: Request):
    if service_name not in SERVICES:
        raise HTTPException(
            status_code=404, detail=f"Service '{service_name}' not found."
        )
    service_url = f"{SERVICES[service_name]}/api/v1/{path}"
    try:
        response = requests.post(service_url, json=await request.json())
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error forwarding request: {e}")


@router.delete("/{service_name}/{path:path}")
async def forward_delete(service_name: str, path: str, request: Request):
    if service_name not in SERVICES:
        raise HTTPException(
            status_code=404, detail=f"Service '{service_name}' not found."
        )
    service_url = f"{SERVICES[service_name]}/api/v1/{path}"
    try:
        response = requests.delete(service_url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error forwarding request: {e}")


app.include_router(router)


@app.get("/health")
def health_check():
    return {"status": "ok", "message": "API Gateway is running."}
