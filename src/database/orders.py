"""Order repository for database operations.

This module provides data access methods for orders.
All database queries related to orders are centralized here.
"""

from datetime import datetime
from typing import Optional
from .connection import get_db


class OrderRepository:
    """Repository for order CRUD operations.
    
    Follows the Repository pattern to abstract database access
    from business logic.
    """
    
    def __init__(self):
        """Initialize with database connection."""
        self.db = get_db()
    
    def create(self, order_data: dict) -> dict:
        """Create a new order.
        
        Args:
            order_data: Dictionary with order details.
            
        Returns:
            Created order with generated ID.
        """
        conn = self.db.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO orders (user_id, items, total, shipping_address, 
                                   payment_method, status, created_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                RETURNING id
            """, (
                order_data['user_id'],
                order_data['items'],
                order_data['total'],
                order_data['shipping_address'],
                order_data['payment_method'],
                order_data['status'],
                datetime.utcnow()
            ))
            
            order_id = cursor.fetchone()[0]
            conn.commit()
            
            return {
                'id': order_id,
                **order_data,
                'created_at': datetime.utcnow().isoformat()
            }
        finally:
            self.db.release_connection(conn)
    
    def get_by_id(self, order_id: str) -> Optional[dict]:
        """Get order by ID.
        
        Args:
            order_id: The order's unique identifier.
            
        Returns:
            Order dictionary or None if not found.
        """
        conn = self.db.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, user_id, items, total, shipping_address,
                       payment_method, status, created_at
                FROM orders
                WHERE id = %s
            """, (order_id,))
            
            row = cursor.fetchone()
            if not row:
                return None
            
            return {
                'id': row[0],
                'user_id': row[1],
                'items': row[2],
                'total': row[3],
                'shipping_address': row[4],
                'payment_method': row[5],
                'status': row[6],
                'created_at': row[7].isoformat()
            }
        finally:
            self.db.release_connection(conn)
    
    def get_by_user(self, user_id: str, limit: int = 10, offset: int = 0) -> list[dict]:
        """Get orders for a specific user.
        
        Args:
            user_id: User's ID.
            limit: Maximum number of orders to return.
            offset: Number of orders to skip (for pagination).
            
        Returns:
            List of order dictionaries.
        """
        conn = self.db.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, user_id, items, total, status, created_at
                FROM orders
                WHERE user_id = %s
                ORDER BY created_at DESC
                LIMIT %s OFFSET %s
            """, (user_id, limit, offset))
            
            orders = []
            for row in cursor.fetchall():
                orders.append({
                    'id': row[0],
                    'user_id': row[1],
                    'items': row[2],
                    'total': row[3],
                    'status': row[4],
                    'created_at': row[5].isoformat()
                })
            return orders
        finally:
            self.db.release_connection(conn)
    
    def update_status(self, order_id: str, status: str) -> bool:
        """Update order status.
        
        Args:
            order_id: Order ID.
            status: New status (pending, processing, shipped, delivered, cancelled).
            
        Returns:
            True if update succeeded, False if order not found.
        """
        conn = self.db.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE orders
                SET status = %s, updated_at = %s
                WHERE id = %s
            """, (status, datetime.utcnow(), order_id))
            
            conn.commit()
            return cursor.rowcount > 0
        finally:
            self.db.release_connection(conn)
