"""
Security utilities for the Carbon Footprint AI Microservice.
Provides API key validation, rate limiting, and authentication.
"""

import os
import secrets
from datetime import datetime, timedelta
from typing import Optional
from functools import wraps

from fastapi import HTTPException, Security, status, Request
from fastapi.security import APIKeyHeader
from slowapi import Limiter
from slowapi.util import get_remote_address
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# ============================================================================
# API Key Authentication
# ============================================================================

API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

# In production, store these in a database or secret manager
# For now, we'll use environment variables
VALID_API_KEYS = set(
    filter(None, os.getenv("VALID_API_KEYS", "").split(","))
)

# Generate a default API key for development
if not VALID_API_KEYS and os.getenv("ENVIRONMENT") == "development":
    DEFAULT_DEV_KEY = "dev_" + secrets.token_urlsafe(32)
    VALID_API_KEYS.add(DEFAULT_DEV_KEY)
    print(f"Development API Key: {DEFAULT_DEV_KEY}")
    print("Add this to your .env file: VALID_API_KEYS={DEFAULT_DEV_KEY}")


async def get_api_key(api_key: str = Security(api_key_header)) -> str:
    """
    Validate API key from request header.
    
    Args:
        api_key: API key from X-API-Key header
        
    Returns:
        str: Validated API key
        
    Raises:
        HTTPException: If API key is invalid or missing
    """
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing API Key. Include 'X-API-Key' header in your request.",
        )
    
    if api_key not in VALID_API_KEYS:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid API Key",
        )
    
    return api_key


def require_api_key(func):
    """
    Decorator to require API key authentication for a route.
    
    Usage:
        @app.get("/protected")
        @require_api_key
        async def protected_route():
            return {"message": "Access granted"}
    """
    @wraps(func)
    async def wrapper(*args, api_key: str = Security(get_api_key), **kwargs):
        return await func(*args, **kwargs)
    return wrapper


# ============================================================================
# Rate Limiting
# ============================================================================

limiter = Limiter(key_func=get_remote_address)

# Rate limit configurations
RATE_LIMITS = {
    "default": "60/minute",
    "prediction": "10/minute",
    "chat": "5/minute",
    "report": "2/minute",
}


def get_rate_limit(endpoint_type: str = "default") -> str:
    """Get rate limit for specific endpoint type."""
    return RATE_LIMITS.get(endpoint_type, RATE_LIMITS["default"])


# ============================================================================
# Secret Validation
# ============================================================================

class SecretValidator:
    """Validate that all required secrets are present."""
    
    REQUIRED_SECRETS = [
        "SECRET_KEY",
        "OPENAI_API_KEY",
    ]
    
    OPTIONAL_SECRETS = [
        "",
        "HUGGINGFACE_API_KEY",
        "AWS_ACCESS_KEY_ID",
        "PINECONE_API_KEY",
    ]
    
    @classmethod
    def validate_required_secrets(cls) -> dict:
        """
        Validate that all required secrets are present.
        
        Returns:
            dict: Status of each secret
            
        Raises:
            ValueError: If any required secret is missing
        """
        missing_secrets = []
        secret_status = {}
        
        for secret in cls.REQUIRED_SECRETS:
            value = os.getenv(secret)
            is_present = bool(value and value != f"your_{secret.lower()}_here")
            secret_status[secret] = is_present
            
            if not is_present:
                missing_secrets.append(secret)
        
        if missing_secrets:
            raise ValueError(
                f"Missing required secrets: {', '.join(missing_secrets)}. "
                f"Please set them in your .env file."
            )
        
        return secret_status
    
    @classmethod
    def check_optional_secrets(cls) -> dict:
        """Check status of optional secrets."""
        secret_status = {}
        
        for secret in cls.OPTIONAL_SECRETS:
            value = os.getenv(secret)
            is_present = bool(value and value != f"your_{secret.lower()}_here")
            secret_status[secret] = is_present
        
        return secret_status
    
    @classmethod
    def get_all_secrets_status(cls) -> dict:
        """Get status of all secrets."""
        return {
            "required": cls.validate_required_secrets(),
            "optional": cls.check_optional_secrets(),
        }


# ============================================================================
# Security Headers
# ============================================================================

def add_security_headers(response):
    """Add security headers to response."""
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    return response


# ============================================================================
# Input Sanitization
# ============================================================================

def sanitize_input(text: str, max_length: int = 1000) -> str:
    """
    Sanitize user input to prevent injection attacks.
    
    Args:
        text: Input text to sanitize
        max_length: Maximum allowed length
        
    Returns:
        str: Sanitized text
    """
    if not text:
        return ""
    
    # Truncate to max length
    text = text[:max_length]
    
    # Remove potentially dangerous characters
    dangerous_chars = ["<", ">", "&", '"', "'", ";", "(", ")", "{", "}"]
    for char in dangerous_chars:
        text = text.replace(char, "")
    
    return text.strip()


# ============================================================================
# Audit Logging
# ============================================================================

class AuditLogger:
    """Log security-relevant events."""
    
    @staticmethod
    def log_api_access(
        endpoint: str,
        api_key: str,
        ip_address: str,
        success: bool = True,
    ):
        """Log API access attempt."""
        timestamp = datetime.now().isoformat()
        status = "SUCCESS" if success else "FAILED"
        masked_key = api_key[:8] + "..." if api_key else "NONE"
        
        log_entry = (
            f"[{timestamp}] API Access {status}: "
            f"endpoint={endpoint}, "
            f"api_key={masked_key}, "
            f"ip={ip_address}"
        )
        
        # In production, send to proper logging service
        print(log_entry)
    
    @staticmethod
    def log_rate_limit_exceeded(endpoint: str, ip_address: str):
        """Log rate limit violation."""
        timestamp = datetime.now().isoformat()
        log_entry = (
            f"[{timestamp}] RATE LIMIT EXCEEDED: "
            f"endpoint={endpoint}, "
            f"ip={ip_address}"
        )
        print(log_entry)


# ============================================================================
# Usage Example
# ============================================================================

if __name__ == "__main__":
    # Validate secrets
    try:
        status = SecretValidator.get_all_secrets_status()
        print("Secret Status:")
        print(f"Required: {status['required']}")
        print(f"Optional: {status['optional']}")
    except ValueError as e:
        print(f"Error: {e}")
