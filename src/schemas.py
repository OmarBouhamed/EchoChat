from pydantic import BaseModel, Field
from typing import Optional 
from datetime import datetime

class EchoRequest(BaseModel):
    """Schema for echo request."""
    message: str = Field(..., min_length=1, max_length=1000)
    
    class Config:
        schema_extra = {
            "example": {
                "message": "Hello, SupportGPT!"
            }
        }
        
class EchoResponse(BaseModel):
    """Schema for echo response."""
    id: str
    message: str
    timestamp: datetime
    
    class Config:
        schema_extra = {
            "example": {
                "id": "echo-123456",
                "message": "Hello, SupportGPT!",
                "timestamp": "2024-01-01T12:00:00Z"
            }
        }       
        
class HealthCheckResponse(BaseModel):
    """Schema for health check response."""
    status: str =  Field(..., pattern="^(healthy|degraded|unhealthy)$")
    version: str
    environment: str