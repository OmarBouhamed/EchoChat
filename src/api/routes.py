from fastapi import APIRouter, HTTPException
from datetime import datetime
import uuid
from ..schemas import EchoRequest, EchoResponse, HealthCheckResponse
from ..config import get_settings


router = APIRouter(prefix="/v1", tags=["v1"])
settings = get_settings()

@router.get("/health", response_model=HealthCheckResponse)
async def health_check():
    """
    Health check endpoint to verify the service is running.
    """
    return HealthCheckResponse(status="healthy", version=settings.app_version, environment=settings.environment)


@router.post("/echo", response_model=EchoResponse)
async def echo_message(request: EchoRequest):
    """ Echo the message back to verify API is working"""
    return EchoResponse(
        id=f"echo-{uuid.uuid4().hex[:81]}",
        message= request.message,
        timestamp=datetime.now()
        )