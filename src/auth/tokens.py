"""JWT token generation and verification.

This module handles JWT (JSON Web Token) operations for authentication.
Tokens are used for stateless authentication between client and server.

Security Note:
    Always use HTTPS in production to protect tokens in transit.
    Keep JWT_SECRET_KEY secure and rotate regularly.
"""

import jwt
import time
from typing import Optional


# In production, load from environment variable
JWT_SECRET_KEY = "your-secret-key-change-in-production"
JWT_ALGORITHM = "HS256"


def create_access_token(user_id: str, expires_in: int = 3600) -> str:
    """Create a JWT access token.
    
    Args:
        user_id: The user's unique identifier.
        expires_in: Token validity duration in seconds (default: 1 hour).
        
    Returns:
        Encoded JWT token string.
        
    Example:
        token = create_access_token("user123", expires_in=7200)
    """
    now = time.time()
    payload = {
        'user_id': user_id,
        'iat': now,  # Issued at
        'exp': now + expires_in,  # Expiration
        'token_type': 'access'
    }
    
    return jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)


def create_refresh_token(user_id: str, expires_in: int = 86400 * 7) -> str:
    """Create a JWT refresh token.
    
    Refresh tokens have longer expiration and can be used to obtain
    new access tokens without re-authentication.
    
    Args:
        user_id: The user's unique identifier.
        expires_in: Token validity duration in seconds (default: 7 days).
        
    Returns:
        Encoded JWT refresh token string.
    """
    now = time.time()
    payload = {
        'user_id': user_id,
        'iat': now,
        'exp': now + expires_in,
        'token_type': 'refresh'
    }
    
    return jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)


def verify_token(token: str) -> Optional[dict]:
    """Verify and decode a JWT token.
    
    Args:
        token: The JWT token string to verify.
        
    Returns:
        Decoded payload dictionary if valid, None if invalid or expired.
        
    Example:
        payload = verify_token(token)
        if payload:
            user_id = payload['user_id']
    """
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def decode_token_unsafe(token: str) -> Optional[dict]:
    """Decode a token without verification.
    
    WARNING: Only use this for debugging or when you need to
    inspect an expired token. Never trust the contents for
    authentication purposes.
    
    Args:
        token: The JWT token string.
        
    Returns:
        Decoded payload without verification.
    """
    try:
        return jwt.decode(token, options={"verify_signature": False})
    except jwt.InvalidTokenError:
        return None
