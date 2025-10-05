"""Authentication middleware for the server."""

import logging
from typing import Optional
from fastapi import HTTPException, Request, status
from fastapi.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware
import os


logger = logging.getLogger(__name__)


class AuthMiddleware(BaseHTTPMiddleware):
    """Middleware for Bearer token authentication."""

    def __init__(self, app, token: Optional[str] = None):
        """Initialize authentication middleware.

        Args:
            app: FastAPI application
            token: Expected bearer token. If None, reads from AUTH_BEARER_TOKEN env var
        """
        super().__init__(app)
        self.token = token or os.getenv("AUTH_BEARER_TOKEN")
        self.disabled = os.getenv("DISABLE_AUTH", "0").lower() in ("1", "true", "yes")

        if not self.disabled and not self.token:
            logger.warning("AUTH_BEARER_TOKEN not set and auth not disabled")

    async def dispatch(self, request: Request, call_next):
        """Process request with authentication check."""
        # Skip authentication for health endpoints
        if request.url.path.startswith("/health"):
            return await call_next(request)

        # Skip authentication if disabled
        if self.disabled:
            return await call_next(request)

        # Check for Authorization header
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Missing authorization header",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Validate Bearer token format
        if not auth_header.startswith("Bearer "):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authorization header format",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Extract and validate token
        provided_token = auth_header[7:].strip()
        if provided_token != self.token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Token is valid, proceed with request
        return await call_next(request)