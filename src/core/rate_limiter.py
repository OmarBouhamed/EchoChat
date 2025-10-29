# Location: src/core/rate_limiter.py
from slowapi import Limiter
from slowapi.util import get_remote_address
from src.config import get_settings

settings = get_settings()

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=[f"{settings.rate_limit_requests}/{settings.rate_limit_period}s"],
)
