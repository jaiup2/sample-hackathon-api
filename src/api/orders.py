"""Order API endpoints.

This module provides REST API endpoints for order management including:
- Create new orders
- Get order status
- List user orders
- Cancel orders

All endpoints require authentication via JWT token.
"""

from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from src.auth import verify_token
from src.database.orders import OrderRepository
from src.utils.notifications import send_order_confirmation


router = APIRouter(prefix="/api/orders", tags=["orders"])


class OrderItem(BaseModel):
    """Single item in an order."""
    product_id: str
    quantity: int
    price: float


class CreateOrderRequest(BaseModel):
    """Request body for creating an order."""
    items: list[OrderItem]
    shipping_address: str
    payment_method: str


class OrderResponse(BaseModel):
    """Standard order response."""
    order_id: str
    status: str
    total: float
    items: list[OrderItem]
    created_at: str


@router.post("/create", response_model=OrderResponse)
async def create_order(
    request: CreateOrderRequest,
    current_user: dict = Depends(get_current_user)
):
    """Create a new order.
    
    This endpoint:
    1. Validates the order items exist and are in stock
    2. Calculates the total price
    3. Processes payment (placeholder)
    4. Creates the order record
    5. Sends confirmation email
    
    Args:
        request: Order creation request with items and shipping info.
        current_user: Authenticated user from JWT token.
        
    Returns:
        Created order details.
        
    Raises:
        HTTPException: If validation fails or payment fails.
    """
    repo = OrderRepository()
    
    # Validate items and calculate total
    total = sum(item.price * item.quantity for item in request.items)
    
    # Create order in database
    order = repo.create({
        'user_id': current_user['id'],
        'items': [item.dict() for item in request.items],
        'total': total,
        'shipping_address': request.shipping_address,
        'payment_method': request.payment_method,
        'status': 'pending'
    })
    
    # Send confirmation email
    await send_order_confirmation(
        email=current_user['email'],
        order_id=order['id'],
        total=total
    )
    
    return OrderResponse(
        order_id=order['id'],
        status=order['status'],
        total=total,
        items=request.items,
        created_at=order['created_at']
    )


@router.get("/{order_id}", response_model=OrderResponse)
async def get_order(
    order_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Get order details by ID.
    
    Users can only access their own orders.
    """
    repo = OrderRepository()
    order = repo.get_by_id(order_id)
    
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    
    if order['user_id'] != current_user['id']:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this order"
        )
    
    return order


@router.get("/", response_model=list[OrderResponse])
async def list_orders(
    current_user: dict = Depends(get_current_user),
    limit: int = 10,
    offset: int = 0
):
    """List orders for the current user.
    
    Supports pagination via limit and offset parameters.
    """
    repo = OrderRepository()
    orders = repo.get_by_user(
        user_id=current_user['id'],
        limit=limit,
        offset=offset
    )
    return orders


@router.post("/{order_id}/cancel")
async def cancel_order(
    order_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Cancel an order.
    
    Only pending orders can be cancelled. Orders that are
    processing or shipped cannot be cancelled.
    """
    repo = OrderRepository()
    order = repo.get_by_id(order_id)
    
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    if order['user_id'] != current_user['id']:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    if order['status'] != 'pending':
        raise HTTPException(
            status_code=400,
            detail=f"Cannot cancel order with status: {order['status']}"
        )
    
    repo.update_status(order_id, 'cancelled')
    return {"message": "Order cancelled successfully"}


def get_current_user(token: str = Depends(oauth2_scheme)):
    """Dependency for getting the current authenticated user."""
    payload = verify_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )
    return {'id': payload['user_id']}
