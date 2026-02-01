

```
# Order API Endpoints Documentation

This document outlines the REST API endpoints for order management in the e-commerce application.

## Endpoints

### 1. Create a New Order

**Endpoint:** `/api/orders/create`

**Method:** `POST`

**Description:** This endpoint allows users to create a new order by providing order items, shipping address, and payment method.

**Request Body:**

```json
{
  "items": [
    {
      "product_id": "string",
      "quantity": number,
      "price": number
    }
  ],
  "shipping_address": "string",
  "payment_method": "string"
}
```

**Response:**

```json
{
  "order_id": "string",
  "status": "string",
  "total": number,
  "items": [
    {
      "product_id": "string",
      "quantity": number,
      "price": number
    }
  ],
  "created_at": "string"
}
```

**Error Handling:**

- `HTTPException` with status code `400` if validation fails.
- `HTTPException` with status code `500` if payment processing fails.

### 2. Get Order Details

**Endpoint:** `/api/orders/{order_id}`

**Method:** `GET`

**Description:** This endpoint retrieves the details of a specific order by its ID. Users can only access their own orders.

**Path Parameters:**

- `order_id` (string): The unique identifier of the order.

**Response:**

```json
{
  "order_id": "string",
  "status": "string",
  "total": number,
  "items": [
    {
      "product_id": "string",
      "quantity": number,
      "price": number
    }
  ],
  "created_at": "string"
}
```

**Error Handling:**

- `HTTPException` with status code `404` if the order is not found.
- `HTTPException` with status code `403` if the user is not authorized to access the order.

### 3. List User Orders

**Endpoint:** `/api/orders/`

**Method:** `GET`

**Description:** This endpoint lists all orders for the current user, supporting pagination via `limit` and `offset` parameters.

**Query Parameters:**

- `limit` (integer, default: 10): The number of orders to return per page.
- `offset` (integer, default: 0): The number of orders to skip before starting to collect the result set.

**Response:**

```json
[
  {
    "order_id": "string",
    "status": "string",
    "total": number,
    "items": [
      {
        "product_id": "string",
        "quantity": number,
        "price": number
      }
    ],
    "created_at": "string"
  }
]
```

**Error Handling:**

- `HTTPException` with status code `400` if invalid parameters are provided.

### 4. Cancel an Order

**Endpoint:** `/api/orders/{order_id}/cancel`

**Method:** `POST`

**Description:** This endpoint allows users to cancel a pending order. Orders that are processing or shipped cannot be cancelled.

**Path Parameters:**

- `order_id` (string): The unique identifier of the order.

**Response:**

```json
{
  "message": "Order cancelled successfully"
}
```

**Error Handling:**

- `HTTPException` with status code `404` if the order is not found.
- `HTTPException` with status code `403` if the user is not authorized to cancel the order.
- `HTTPException` with status code `400` if the order status is not 'pending'.
```

## Flowchart

```mermaid
graph TD
    A[Start] --> B[Create New Order]
    B --> C{Order Exists?}
    C -- Yes --> D[Order Details Retrieved]
    C -- No --> E[Order Created]
    D --> F[Get Order Details]
    F --> G{Order Found?}
    G -- Yes --> H[Order Details Retrieved]
    G -- No --> I[Order Not Found]
    I --> J[List User Orders]
    J --> K{Orders Found?}
    K -- Yes --> L[Orders Listed]
    K -- No --> M[No Orders Found]
    E --> N[Cancel Order]
    N --> O{Order Found?}
    O -- Yes --> P[Order Cancelled]
    O -- No --> Q[Order Not Found]
    P --> R[End]
    I --> R
    M --> R
    H --> R
    L --> R
```

## Dependencies

- `verify_token`: Function to verify JWT token.
- `send_order_confirmation`: Function to send order confirmation email.
- `OrderRepository`: Database repository for order management.
- `get_current_user`: Dependency for getting the current authenticated user.
```

## Payment Processing

The payment processing is handled by the `PaymentProcessor` class in the `payments/processor.py` module. It supports multiple payment providers and transaction management.

```python
class PaymentProcessor:
    def __init__(self, provider: PaymentProvider = PaymentProvider.STRIPE):
        self.provider = provider

    # Payment processing methods go here
```

## Notes

- All endpoints require authentication via JWT token.
- The `create_order` endpoint validates the order items exist and are in stock, calculates the total price, processes payment, creates the order record, and sends a confirmation email.
- The `cancel_order` endpoint only allows pending orders to be cancelled.
- The `list_orders` endpoint supports pagination via `limit` and `offset` parameters.
```