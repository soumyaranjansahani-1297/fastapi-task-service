import redis
from fastapi import Request, HTTPException

redis_client = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True
)

LIMIT = 5
WINDOW = 60

async def rate_limit(request: Request):

    client_ip = request.client.host

    key = f"rate_limit:{client_ip}"

    current = redis_client.incr(key)

    if current == 1:
        redis_client.expire(key, WINDOW)

    if current > LIMIT:
        raise HTTPException(
            status_code=429,
            detail="Rate limit exceeded. Try again later."
        )