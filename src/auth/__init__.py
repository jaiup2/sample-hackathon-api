"""Authentication module.

This module provides user authentication functionality including:
- Traditional email/password authentication
- OAuth2 integration (Google, GitHub)
- JWT token management
- Session handling with Redis

Quick Start:
    from src.auth import AuthManager
    
    auth = AuthManager(db, redis)
    user = auth.login("user@example.com", "password")
    token = auth.create_session(user)
"""

from .login import AuthManager, AuthenticationError
from .tokens import create_access_token, verify_token
from .oauth import OAuth2Provider, GoogleOAuth2, GitHubOAuth2

__all__ = [
    'AuthManager',
    'AuthenticationError',
    'create_access_token',
    'verify_token',
    'OAuth2Provider',
    'GoogleOAuth2',
    'GitHubOAuth2'
]
