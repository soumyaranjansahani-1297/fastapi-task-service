import os

from fastapi import Request, HTTPException
from redis.asyncio import Redis
from redis.exceptions import RedisError

from app.logger import logger

redis_client = Redis(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=int(os.getenv("REDIS_PORT", "6379")),
    decode_responses=True
)

LIMIT = int(os.getenv("RATE_LIMIT_REQUESTS", "5"))
WINDOW = int(os.getenv("RATE_LIMIT_WINDOW_SECONDS", "60"))

async def rate_limit(request: Request):

    client_ip = request.client.host if request.client else "unknown"

    key = f"rate_limit:{client_ip}"

    try:
        current = await redis_client.incr(key)

        if current == 1:
            await redis_client.expire(key, WINDOW)
    except RedisError:
        logger.exception("Redis is unavailable for rate limiting")
        raise HTTPException(
            status_code=503,
            detail="Rate limiter unavailable. Try again later."
        )

    if current > LIMIT:
        logger.warning("Rate limit exceeded for client_ip=%s", client_ip)
        raise HTTPException(
            status_code=429,
            detail="Rate limit exceeded. Try again later."
        )
