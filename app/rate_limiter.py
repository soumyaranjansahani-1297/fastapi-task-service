import time
import os
from dotenv import load_dotenv
from fastapi import Request, HTTPException

load_dotenv()

request_log = {}

LIMIT = int(os.getenv("RATE_LIMIT_REQUESTS", 5))
WINDOW = int(os.getenv("RATE_LIMIT_WINDOW_SECONDS", 60))

async def rate_limit(request: Request):

    client_ip = request.client.host
    current_time = time.time()

    if client_ip not in request_log:
        request_log[client_ip] = []

    request_log[client_ip] = [
        timestamp
        for timestamp in request_log[client_ip]
        if current_time - timestamp < WINDOW
    ]

    if len(request_log[client_ip]) >= LIMIT:
        raise HTTPException(
            status_code=429,
            detail="Rate limit exceeded. Try again later."
        )

    request_log[client_ip].append(current_time)