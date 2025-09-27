"""
Request Limiter configurations
"""

import os
import time

from functools import wraps

from fastapi import HTTPException

from db.redis.broker import redis_client


class RequestLimiter:
    """
    Implements rate limiting using Redis to track requests by client IP
    and request type.
    """

    def __init__(self):
        """
        Initialize with rate limit settings from environment variables.
        - LIMIT_GET: Maximum allowed requests for GET requests.
        - LIMIT_PPD: Maximum allowed requests for PATCH, POST, DELETE requests.
        - TIME_GET: Time window (in seconds) for GET requests.
        - TIME_PPD: Time window (in seconds) for PATCH, POST, DELETE requests.
        """
        self.LIMIT_GET = int(os.getenv("LIMIT_GET"))
        self.LIMIT_PPD = int(os.getenv("LIMIT_PPD"))
        self.TIME_GET = int(os.getenv("TIME_GET"))
        self.TIME_PPD = int(os.getenv("TIME_PPD"))

    def limiter(self, max_requests: int, period: int):
        """
        Creates a decorator to limit the rate of requests to an API endpoint.

        Arguments:
        - max_requests: The maximum number of requests allowed within a given period.
        - period: The time window in seconds during which the requests are counted.

        Returns:
        - A decorator function that can be applied to a FastAPI route handler.
        """
        def decorator(func):
            @wraps(func)
            async def wrapper(*args, **kwargs):
                request = kwargs.get("request")
                if not request:
                    raise HTTPException(
                        status_code=400,
                        detail="Request object is missing"
                    )

                client_ip = request.client.host
                current_time = int(time.time() // period)
                action = func.__name__
                redis_key = f"throttle:{client_ip}:{action}:{current_time}"
                request_count = redis_client.get(redis_key)

                if request_count and int(request_count) >= max_requests:
                    raise HTTPException(
                        status_code=429,
                        detail="Too many requests. Please try again later"
                    )

                redis_client.incr(redis_key)
                redis_client.expire(redis_key, period)

                return await func(*args, **kwargs)

            return wrapper

        return decorator

    def get_limiter(self):
        """
        Return a decorator to rate limit GET requests per configured limits.

        Returns:
        - A decorator function that can be applied to GET route handlers.
        """
        return self.limiter(self.LIMIT_GET, self.TIME_GET)

    def ppd_limiter(self):
        """
        Return a decorator to rate limit PATCH, POST, and DELETE requests.

        Returns:
            A decorator for PATCH, POST, or DELETE route handlers.
        """

        return self.limiter(self.LIMIT_PPD, self.TIME_PPD)


limiter = RequestLimiter()
