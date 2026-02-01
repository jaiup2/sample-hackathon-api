"""Database connection and configuration.

This module sets up database connections for PostgreSQL (primary storage)
and Redis (caching and sessions).

Configuration is loaded from environment variables:
- DATABASE_URL: PostgreSQL connection string
- REDIS_URL: Redis connection string
"""

import os
from functools import lru_cache


class DatabaseConnection:
    """PostgreSQL database connection manager.
    
    Uses connection pooling for efficient database access.
    """
    
    def __init__(self, connection_url: str = None):
        """Initialize database connection.
        
        Args:
            connection_url: PostgreSQL connection URL.
                           If not provided, uses DATABASE_URL env var.
        """
        self.url = connection_url or os.getenv("DATABASE_URL")
        self._pool = None
    
    def connect(self):
        """Establish database connection pool."""
        import psycopg2.pool
        self._pool = psycopg2.pool.ThreadedConnectionPool(
            minconn=1,
            maxconn=10,
            dsn=self.url
        )
    
    def get_connection(self):
        """Get a connection from the pool."""
        if not self._pool:
            self.connect()
        return self._pool.getconn()
    
    def release_connection(self, conn):
        """Return a connection to the pool."""
        self._pool.putconn(conn)
    
    def close(self):
        """Close all connections in the pool."""
        if self._pool:
            self._pool.closeall()


class RedisConnection:
    """Redis connection for caching and sessions.
    
    Used for:
    - Session storage (see auth module)
    - Query result caching
    - Rate limiting
    """
    
    def __init__(self, redis_url: str = None):
        """Initialize Redis connection.
        
        Args:
            redis_url: Redis connection URL.
                      If not provided, uses REDIS_URL env var.
        """
        self.url = redis_url or os.getenv("REDIS_URL", "redis://localhost:6379")
        self._client = None
    
    @property
    def client(self):
        """Get the Redis client (lazy initialization)."""
        if self._client is None:
            import redis
            self._client = redis.from_url(self.url)
        return self._client
    
    def get(self, key: str):
        """Get a value from Redis."""
        return self.client.get(key)
    
    def set(self, key: str, value: str, ex: int = None):
        """Set a value in Redis with optional expiration."""
        return self.client.set(key, value, ex=ex)
    
    def setex(self, key: str, seconds: int, value: str):
        """Set a value with expiration in seconds."""
        return self.client.setex(key, seconds, value)
    
    def delete(self, key: str):
        """Delete a key from Redis."""
        return self.client.delete(key)


@lru_cache()
def get_db() -> DatabaseConnection:
    """Get the singleton database connection."""
    db = DatabaseConnection()
    db.connect()
    return db


@lru_cache()
def get_redis() -> RedisConnection:
    """Get the singleton Redis connection."""
    return RedisConnection()
