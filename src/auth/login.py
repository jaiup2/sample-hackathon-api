"""Authentication module for user login and registration.

This module handles all authentication-related functionality including:
- User login with email/password
- OAuth2 integration for third-party authentication
- Session management with Redis
"""

from typing import Optional
from .tokens import create_access_token, verify_token
from .oauth import OAuth2Provider


class AuthenticationError(Exception):
    """Raised when authentication fails."""
    pass


class AuthManager:
    """Manages user authentication.
    
    This is the main entry point for authentication operations.
    It supports both traditional email/password and OAuth2 flows.
    
    Example:
        auth = AuthManager()
        user = auth.login("user@example.com", "password123")
        token = auth.create_session(user)
    """
    
    def __init__(self, db_connection, redis_client):
        """Initialize the authentication manager.
        
        Args:
            db_connection: Database connection for user lookups.
            redis_client: Redis client for session storage.
        """
        self.db = db_connection
        self.redis = redis_client
        self.oauth_providers = {}
    
    def register_oauth_provider(self, name: str, provider: OAuth2Provider):
        """Register an OAuth2 provider.
        
        Args:
            name: Provider name (e.g., 'google', 'github').
            provider: OAuth2Provider instance.
        """
        self.oauth_providers[name] = provider
    
    def login(self, email: str, password: str) -> dict:
        """Authenticate user with email and password.
        
        Args:
            email: User's email address.
            password: User's password (will be hashed for comparison).
            
        Returns:
            User dictionary if authentication succeeds.
            
        Raises:
            AuthenticationError: If credentials are invalid.
        """
        user = self.db.users.find_one({'email': email})
        if not user:
            raise AuthenticationError("Invalid email or password")
        
        if not self._verify_password(password, user['password_hash']):
            raise AuthenticationError("Invalid email or password")
        
        return self._sanitize_user(user)
    
    def login_oauth(self, provider_name: str, auth_code: str) -> dict:
        """Authenticate user via OAuth2.
        
        Args:
            provider_name: Name of the OAuth provider.
            auth_code: Authorization code from OAuth flow.
            
        Returns:
            User dictionary.
        """
        provider = self.oauth_providers.get(provider_name)
        if not provider:
            raise AuthenticationError(f"Unknown provider: {provider_name}")
        
        # Exchange code for user info
        user_info = provider.exchange_code(auth_code)
        
        # Find or create user
        user = self.db.users.find_one({'oauth_id': user_info['id']})
        if not user:
            user = self.db.users.create({
                'email': user_info['email'],
                'name': user_info['name'],
                'oauth_id': user_info['id'],
                'oauth_provider': provider_name
            })
        
        return self._sanitize_user(user)
    
    def create_session(self, user: dict, expires_in: int = 3600) -> str:
        """Create a session token for the user.
        
        Args:
            user: User dictionary.
            expires_in: Token expiration time in seconds.
            
        Returns:
            JWT access token.
        """
        token = create_access_token(user['id'], expires_in)
        
        # Store session in Redis for tracking
        self.redis.setex(
            f"session:{user['id']}",
            expires_in,
            token
        )
        
        return token
    
    def verify_session(self, token: str) -> Optional[dict]:
        """Verify a session token and return user info.
        
        Args:
            token: JWT token to verify.
            
        Returns:
            User dictionary if valid, None otherwise.
        """
        payload = verify_token(token)
        if not payload:
            return None
        
        # Check if session exists in Redis
        user_id = payload['user_id']
        stored_token = self.redis.get(f"session:{user_id}")
        
        if not stored_token or stored_token.decode() != token:
            return None
        
        return self.db.users.find_by_id(user_id)
    
    def logout(self, user_id: str):
        """Log out a user by invalidating their session.
        
        Args:
            user_id: User's ID.
        """
        self.redis.delete(f"session:{user_id}")
    
    def _verify_password(self, password: str, password_hash: str) -> bool:
        """Verify password against hash."""
        import hashlib
        test_hash = hashlib.sha256(password.encode()).hexdigest()
        return test_hash == password_hash
    
    def _sanitize_user(self, user: dict) -> dict:
        """Remove sensitive fields from user dict."""
        safe_fields = ['id', 'email', 'name', 'created_at']
        return {k: v for k, v in user.items() if k in safe_fields}
