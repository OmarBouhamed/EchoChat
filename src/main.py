# Location: src/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from src.config import get_settings
from src.core.logger import logger
from src.core.rate_limiter import limiter
from src.db.database import init_db, close_db
from src.cache.redis_client import redis_client
from src.api import routes
from src.api.conversations import router as conversation_router

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Production-grade RAG Chatbot with FastAPI, LangGraph, and Qdrant",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Add rate limiter
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if settings.debug else ["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(routes.router)
app.include_router(conversation_router)

@app.on_event("startup")
async def startup_event():
    """Run on application startup."""
    logger.info(f"🚀 {settings.app_name} starting up...")
    logger.info(f"Environment: {settings.environment}")
    logger.info(f"Debug mode: {settings.debug}")
    
    # Initialize database
    await init_db()
    
    # Connect to Redis
    await redis_client.connect()

@app.on_event("shutdown")
async def shutdown_event():
    """Run on application shutdown."""
    logger.info(f"🛑 {settings.app_name} shutting down...")
    
    # Disconnect from Redis
    await redis_client.disconnect()
