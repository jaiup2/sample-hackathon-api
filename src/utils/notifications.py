"""Notification utilities.

This module provides notification functionality including:
- Email notifications via SendGrid
- SMS notifications (future)
- Push notifications (future)
"""

import os
import asyncio
from typing import Optional


class NotificationService:
    """Service for sending various types of notifications."""
    
    def __init__(self):
        """Initialize notification service."""
        self.sendgrid_api_key = os.getenv("SENDGRID_API_KEY")
        self.from_email = os.getenv("FROM_EMAIL", "noreply@example.com")
    
    async def send_email(
        self,
        to: str,
        subject: str,
        body: str,
        html: Optional[str] = None
    ):
        """Send an email notification.
        
        Args:
            to: Recipient email address.
            subject: Email subject.
            body: Plain text body.
            html: Optional HTML body.
        """
        # In production, use sendgrid.SendGridAPIClient
        print(f"📧 Sending email to {to}: {subject}")
        # Simulate async email sending
        await asyncio.sleep(0.1)


_service = NotificationService()


async def send_order_confirmation(email: str, order_id: str, total: float):
    """Send order confirmation email.
    
    Args:
        email: Customer's email address.
        order_id: Order ID for reference.
        total: Order total amount.
    """
    subject = f"Order Confirmation - #{order_id}"
    body = f"""
Thank you for your order!

Order ID: {order_id}
Total: ${total:.2f}

We'll notify you when your order ships.

Thank you for shopping with us!
"""
    
    await _service.send_email(email, subject, body)


async def send_shipping_notification(email: str, order_id: str, tracking_number: str):
    """Send shipping notification with tracking info.
    
    Args:
        email: Customer's email address.
        order_id: Order ID.
        tracking_number: Shipping tracking number.
    """
    subject = f"Your Order #{order_id} Has Shipped!"
    body = f"""
Great news! Your order is on its way.

Order ID: {order_id}
Tracking Number: {tracking_number}

Track your package at: https://track.example.com/{tracking_number}
"""
    
    await _service.send_email(email, subject, body)


async def send_password_reset(email: str, reset_token: str):
    """Send password reset email.
    
    Args:
        email: User's email address.
        reset_token: Password reset token.
    """
    subject = "Password Reset Request"
    body = f"""
You requested a password reset.

Click here to reset your password:
https://example.com/reset-password?token={reset_token}

If you didn't request this, please ignore this email.

This link expires in 1 hour.
"""
    
    await _service.send_email(email, subject, body)
