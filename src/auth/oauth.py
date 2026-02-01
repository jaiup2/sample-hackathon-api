"""OAuth2 integration for third-party authentication.

Supports multiple OAuth2 providers including Google and GitHub.
Each provider is configured separately with their own credentials.

Configuration:
    GOOGLE_CLIENT_ID: Your Google OAuth2 client ID
    GOOGLE_CLIENT_SECRET: Your Google OAuth2 client secret
    GITHUB_CLIENT_ID: Your GitHub OAuth2 client ID
    GITHUB_CLIENT_SECRET: Your GitHub OAuth2 client secret
"""

import requests
from typing import Optional
from abc import ABC, abstractmethod


class OAuth2Provider(ABC):
    """Base class for OAuth2 providers."""
    
    @abstractmethod
    def get_auth_url(self, redirect_uri: str, state: str) -> str:
        """Generate the authorization URL for this provider."""
        pass
    
    @abstractmethod
    def exchange_code(self, code: str, redirect_uri: str) -> dict:
        """Exchange authorization code for user info."""
        pass


class GoogleOAuth2(OAuth2Provider):
    """Google OAuth2 provider implementation.
    
    Used for "Sign in with Google" functionality.
    Provides access to user's email and profile information.
    """
    
    AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
    TOKEN_URL = "https://oauth2.googleapis.com/token"
    USER_INFO_URL = "https://www.googleapis.com/oauth2/v2/userinfo"
    
    def __init__(self, client_id: str, client_secret: str):
        self.client_id = client_id
        self.client_secret = client_secret
    
    def get_auth_url(self, redirect_uri: str, state: str) -> str:
        """Generate Google OAuth2 authorization URL."""
        params = {
            'client_id': self.client_id,
            'redirect_uri': redirect_uri,
            'response_type': 'code',
            'scope': 'email profile',
            'state': state,
            'access_type': 'offline'
        }
        query = '&'.join(f"{k}={v}" for k, v in params.items())
        return f"{self.AUTH_URL}?{query}"
    
    def exchange_code(self, code: str, redirect_uri: str) -> dict:
        """Exchange Google auth code for user information."""
        # Exchange code for access token
        token_response = requests.post(self.TOKEN_URL, data={
            'code': code,
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'redirect_uri': redirect_uri,
            'grant_type': 'authorization_code'
        })
        
        token_data = token_response.json()
        access_token = token_data['access_token']
        
        # Get user info
        user_response = requests.get(
            self.USER_INFO_URL,
            headers={'Authorization': f'Bearer {access_token}'}
        )
        
        user_data = user_response.json()
        return {
            'id': user_data['id'],
            'email': user_data['email'],
            'name': user_data.get('name', user_data['email']),
            'picture': user_data.get('picture')
        }


class GitHubOAuth2(OAuth2Provider):
    """GitHub OAuth2 provider implementation.
    
    Used for "Sign in with GitHub" functionality.
    Popular choice for developer-focused applications.
    """
    
    AUTH_URL = "https://github.com/login/oauth/authorize"
    TOKEN_URL = "https://github.com/login/oauth/access_token"
    USER_INFO_URL = "https://api.github.com/user"
    
    def __init__(self, client_id: str, client_secret: str):
        self.client_id = client_id
        self.client_secret = client_secret
    
    def get_auth_url(self, redirect_uri: str, state: str) -> str:
        """Generate GitHub OAuth2 authorization URL."""
        params = {
            'client_id': self.client_id,
            'redirect_uri': redirect_uri,
            'scope': 'user:email',
            'state': state
        }
        query = '&'.join(f"{k}={v}" for k, v in params.items())
        return f"{self.AUTH_URL}?{query}"
    
    def exchange_code(self, code: str, redirect_uri: str) -> dict:
        """Exchange GitHub auth code for user information."""
        # Exchange code for access token
        token_response = requests.post(
            self.TOKEN_URL,
            data={
                'code': code,
                'client_id': self.client_id,
                'client_secret': self.client_secret,
                'redirect_uri': redirect_uri
            },
            headers={'Accept': 'application/json'}
        )
        
        token_data = token_response.json()
        access_token = token_data['access_token']
        
        # Get user info
        user_response = requests.get(
            self.USER_INFO_URL,
            headers={
                'Authorization': f'token {access_token}',
                'Accept': 'application/json'
            }
        )
        
        user_data = user_response.json()
        return {
            'id': str(user_data['id']),
            'email': user_data.get('email'),
            'name': user_data.get('name', user_data['login']),
            'avatar': user_data.get('avatar_url')
        }


def create_provider(name: str, client_id: str, client_secret: str) -> Optional[OAuth2Provider]:
    """Factory function to create OAuth2 providers.
    
    Args:
        name: Provider name ('google' or 'github').
        client_id: OAuth2 client ID.
        client_secret: OAuth2 client secret.
        
    Returns:
        OAuth2Provider instance or None if unknown provider.
    """
    providers = {
        'google': GoogleOAuth2,
        'github': GitHubOAuth2
    }
    
    provider_class = providers.get(name.lower())
    if provider_class:
        return provider_class(client_id, client_secret)
    return None
