from fastapi import APIRouter
import httpx

router = APIRouter()

@router.get("/health")
async def health_check():
    return {"status": "ok", "service": "banking-service"}

@router.get("/health/dependency")
async def check_auth_service():
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get("http://auth-service:8063/health")
            return {
                "auth-service-status": response.json(),
                "status": "connected"
            }
    except Exception as e:
        return {"status": "error", "detail": str(e)}