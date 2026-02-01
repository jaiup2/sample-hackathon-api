

[Module Documentation]:

# Module Documentation

## src/api/orders.py

### Overview

The `orders.py` module provides REST API endpoints for order management in an e-commerce application. It includes endpoints for creating new orders, getting order status, listing user orders, and canceling orders. All endpoints require authentication via JWT token.

### Imported Modules

- `fastapi`: A modern, fast (high-performance), web framework for building APIs with Python 3.6+ based on standard Python type hints.
- `pydantic`: A data validation library for Python, based on pydantic's data validation and settings management.
- `src.auth`: A module containing functions for verifying JWT tokens.
- `src.database.orders`: A module providing database operations for order management.
- `src.utils.notifications`: A module containing functions for sending notifications, such as order confirmation emails.

### Code Blocks

1. **OrderItem Class**

    ```python
    class OrderItem(BaseModel):
        """Single item in an order."""
        product_id: str
        quantity: int
        price: float
    ```

    The `OrderItem` class represents a single item in an order, containing attributes for product ID, quantity, and price.

2. **CreateOrderRequest Class**

    ```python
    class CreateOrderRequest(BaseModel):
        """Request body for creating an order."""
        items: list[OrderItem]
        shipping_address: str
        payment_method: str
    ```

    The `CreateOrderRequest` class represents the request body for creating an order, containing attributes for order items, shipping address, and payment method.

3. **OrderResponse Class**

    ```python
    class OrderResponse(BaseModel):
        """Standard order response."""
        order_id: str
        status: str
        total: float
        items: list[OrderItem]
        created_at: str
    ```

    The `OrderResponse` class represents the standard response for order-related operations, containing attributes for order ID, status, total price, order items, and creation timestamp.

4. **create_order Function**

    ```python
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
    ```

    The `create_order` function handles the creation of a new order, validating order items, calculating the total price, processing payment, creating the order record, and sending a confirmation email.

5. **get_order Function**

    ```python
    @router.get("/{order_id}", response_model=OrderResponse)
    async def get_order(
        order_id: str,
        current_user: dict = Depends(get_current_user)
    ):
        """Get order details by ID.
        
        Users can only access their own orders.
    ```

    The `get_order` function retrieves order details by ID, ensuring that users can only access their own orders.

6. **list_orders Function**

    ```python
    @router.get("/", response_model=list[OrderResponse])
    async def list_orders(
        current_user: dict = Depends(get_current_user),
        limit: int = 10,
        offset: int = 0
    ):
        """List orders for the current user.
        
        Supports pagination via limit and offset parameters.
    ```

    The `list_orders` function lists orders for the current user, supporting pagination via limit and offset parameters.

7. **cancel_order Function**

    ```python
    @router.post("/{order_id}/cancel")
    async def cancel_order(
        order_id: str,
        current_user: dict = Depends(get_current_user)
    ):
        """Cancel an order.
        
        Only pending orders can be cancelled. Orders that are
        processing or shipped cannot be cancelled.
    ```

    The `cancel_order` function cancels an order, ensuring that only pending orders can be cancelled.

8. **get_current_user Function**

    ```python
    def get_current_user(token: str = Depends(oauth2_scheme)):
        """Dependency for getting the current authenticated user."""
        payload = verify_token(token)
        if not payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token"
            )
        return {'id': payload['user_id']}
    ```

    The `get_current_user` function is a dependency for obtaining the current authenticated user, verifying the JWT token and returning the user ID.

## src/payments/processor.py

### Overview

The `processor.py` module handles payment processing for the e-commerce API, supporting multiple payment providers and transaction management.

### Imported Modules

- `typing`: A built-in Python module for type hinting.
- `dataclasses`: A built-in Python module for creating data classes.
- `enum`: A built-in Python module for creating enumerations.

### Code Blocks

1. **PaymentStatus Enum**

    ```python
    class PaymentStatus(Enum):
        """Payment transaction status."""
        PENDING = "pending"
        PROCESSING = "processing"
        COMPLETED = "completed"
        FAILED = "failed"
        REFUNDED = "refunded"
    ```

    The `PaymentStatus` enumeration defines the possible statuses for a payment transaction.

2. **PaymentProvider Enum**

    ```python
    class PaymentProvider(Enum):
        """Supported payment providers."""
        STRIPE = "stripe"
        PAYPAL = "paypal"
        SQUARE = "square"
    ```

    The `PaymentProvider` enumeration defines the supported payment providers.

3. **PaymentTransaction Dataclass**

    ```python
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
    ```

    The `PaymentTransaction` data class represents a payment transaction, containing attributes for transaction ID, order ID, amount, currency, provider, status, and customer ID.

4. **PaymentProcessor Class**

    ```python
    class PaymentProcessor:
        """Handles payment processing operations."""
        
        def __init__(self, provider: PaymentProvider = PaymentProvider.STRIPE):
            """Initialize payment processor.
            
            Args:
                provider: Payment provider to use.
        ```

    The `PaymentProcessor` class handles payment processing operations, initialized with a specified payment provider.