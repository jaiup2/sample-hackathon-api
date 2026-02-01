

```markdown
# Function Documentation

## create_order

**Function Signature:**
```python
async def create_order(
    request: CreateOrderRequest,
    current_user: dict = Depends(get_current_user)
):
```

**Parameters:**
- `request`: An instance of `CreateOrderRequest` containing the order items and shipping information.
  - `items`: A list of `OrderItem` objects, each with `product_id`, `quantity`, and `price`.
  - `shipping_address`: The shipping address for the order.
  - `payment_method`: The payment method for the order.
- `current_user`: An authenticated user dictionary obtained from the JWT token.

**Returns:**
- An instance of `OrderResponse` containing the order details, including `order_id`, `status`, `total`, `items`, and `created_at`.

**Raises:**
- `HTTPException`: If validation fails or payment processing fails.

**Description:**
This function creates a new order by validating the order items, calculating the total price, processing payment (placeholder), creating the order record in the database, and sending a confirmation email.

## get_order

**Function Signature:**
```python
async def get_order(
    order_id: str,
    current_user: dict = Depends(get_current_user)
):
```

**Parameters:**
- `order_id`: The unique identifier of the order to retrieve.
- `current_user`: An authenticated user dictionary obtained from the JWT token.

**Returns:**
- An instance of `OrderResponse` containing the order details.

**Raises:**
- `HTTPException`: If the order is not found or the user is not authorized to access the order.

**Description:**
This function retrieves the details of a specific order by its ID. Users can only access their own orders.

## list_orders

**Function Signature:**
```python
async def list_orders(
    current_user: dict = Depends(get_current_user),
    limit: int = 10,
    offset: int = 0
):
```

**Parameters:**
- `current_user`: An authenticated user dictionary obtained from the JWT token.
- `limit`: The maximum number of orders to return (default is 10).
- `offset`: The number of orders to skip before starting to collect the result set (default is 0).

**Returns:**
- A list of `OrderResponse` objects representing the user's orders.

**Raises:**
- `HTTPException`: If the user is not found.

**Description:**
This function lists the orders for the current user, supporting pagination via `limit` and `offset` parameters.

## cancel_order

**Function Signature:**
```python
async def cancel_order(
    order_id: str,
    current_user: dict = Depends(get_current_user)
):
```

**Parameters:**
- `order_id`: The unique identifier of the order to cancel.
- `current_user`: An authenticated user dictionary obtained from the JWT token.

**Returns:**
- A dictionary with a message indicating the order was cancelled successfully.

**Raises:**
- `HTTPException`: If the order is not found, the user is not authorized, or the order status is not 'pending'.

**Description:**
This function cancels an order. Only pending orders can be cancelled. Orders that are processing or shipped cannot be cancelled.
```