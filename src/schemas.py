from pydantic import BaseModel, Field
from typing import Optional, List
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
    

# ===== CONVERSATION ENDPOINTS (Week 2) =====

class MessageCreate(BaseModel):
    """Create message request."""
    content: str = Field(..., min_length=1, max_length=10000)
    
    class Config:
        json_schema_extra = {
            "example": {
                "content": "How do I reset my password?"
            }
        }

class MessageResponse(BaseModel):
    """Message response."""
    id: str
    conversation_id: str
    role: str  # "user" or "assistant"
    content: str
    created_at: datetime
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": "msg-001",
                "conversation_id": "conv-001",
                "role": "user",
                "content": "How do I reset my password?",
                "created_at": "2025-10-29T12:00:00"
            }
        }

class ConversationCreate(BaseModel):
    """Create conversation request."""
    title: Optional[str] = Field(None, max_length=200)
    
    class Config:
        json_schema_extra = {
            "example": {
                "title": "Account Recovery"
            }
        }

class ConversationResponse(BaseModel):
    """Conversation response."""
    id: str
    user_id: str
    title: Optional[str]
    created_at: datetime
    updated_at: datetime
    messages: List[MessageResponse] = []
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": "conv-001",
                "user_id": "user-123",
                "title": "Account Recovery",
                "created_at": "2025-10-29T12:00:00",
                "updated_at": "2025-10-29T12:00:00",
                "messages": []
            }
        }