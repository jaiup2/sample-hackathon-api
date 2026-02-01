"""Payment Processing Module.

This module handles payment processing for the e-commerce API.
Supports multiple payment providers and transaction management.
"""

from typing import Optional
from dataclasses import dataclass
from enum import Enum


class PaymentStatus(Enum):
    """Payment transaction status."""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    REFUNDED = "refunded"


class PaymentProvider(Enum):
    """Supported payment providers."""
    STRIPE = "stripe"
    PAYPAL = "paypal"
    SQUARE = "square"


@dataclass
class PaymentTransaction:
    """Represents a payment transaction."""
    transaction_id: str
    order_id: str
    amount: float
    currency: str
    provider: PaymentProvider
    status: PaymentStatus
    customer_id: Optional[str] = None


class PaymentProcessor:
    """Handles payment processing operations."""
    
    def __init__(self, provider: PaymentProvider = PaymentProvider.STRIPE):
        """Initialize payment processor.
        
        Args:
            provider: Payment provider to use
        """
        self.provider = provider
        self._api_key = None
    
    def configure(self, api_key: str) -> None:
        """Configure the payment processor with API credentials.
        
        Args:
            api_key: API key for the payment provider
        """
        self._api_key = api_key
    
    def create_payment(
        self,
        order_id: str,
        amount: float,
        currency: str = "USD",
        customer_id: Optional[str] = None
    ) -> PaymentTransaction:
        """Create a new payment transaction.
        
        Args:
            order_id: Associated order ID
            amount: Payment amount
            currency: Currency code (default: USD)
            customer_id: Optional customer ID
            
        Returns:
            PaymentTransaction object
        """
        import uuid
        transaction_id = f"txn_{uuid.uuid4().hex[:12]}"
        
        return PaymentTransaction(
            transaction_id=transaction_id,
            order_id=order_id,
            amount=amount,
            currency=currency,
            provider=self.provider,
            status=PaymentStatus.PENDING,
            customer_id=customer_id
        )
    
    def process_payment(self, transaction: PaymentTransaction) -> PaymentTransaction:
        """Process a pending payment.
        
        Args:
            transaction: Transaction to process
            
        Returns:
            Updated transaction with new status
        """
        # Simulate payment processing
        transaction.status = PaymentStatus.PROCESSING
        
        # In real implementation, call payment provider API
        # For demo, assume success
        transaction.status = PaymentStatus.COMPLETED
        
        return transaction
    
    def refund_payment(self, transaction: PaymentTransaction) -> PaymentTransaction:
        """Refund a completed payment.
        
        Args:
            transaction: Transaction to refund
            
        Returns:
            Updated transaction with refunded status
        """
        if transaction.status != PaymentStatus.COMPLETED:
            raise ValueError("Can only refund completed payments")
        
        transaction.status = PaymentStatus.REFUNDED
        return transaction
    
    def get_transaction_status(self, transaction_id: str) -> PaymentStatus:
        """Get the status of a transaction.
        
        Args:
            transaction_id: Transaction ID to check
            
        Returns:
            Current transaction status
        """
        # In real implementation, query payment provider
        return PaymentStatus.PENDING


def create_checkout_session(
    order_id: str,
    amount: float,
    currency: str = "USD"
) -> dict:
    """Create a checkout session for a customer.
    
    Args:
        order_id: Order ID for the checkout
        amount: Total amount to charge
        currency: Currency code
        
    Returns:
        Checkout session details
    """
    processor = PaymentProcessor()
    transaction = processor.create_payment(order_id, amount, currency)
    
    return {
        "session_id": transaction.transaction_id,
        "order_id": order_id,
        "amount": amount,
        "currency": currency,
        "status": transaction.status.value,
        "checkout_url": f"/checkout/{transaction.transaction_id}"
    }
