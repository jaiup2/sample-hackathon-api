

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
    A[Start] --> B[Create Order]
    B --> C{Order Exists?}
    C -- Yes --> D[Validate Items & Calculate Total]
    C -- No --> E[HTTP 400]
    D --> F[Process Payment]
    F --> G{Payment Successful?}
    G -- Yes --> H[Create Order in Database]
    G -- No --> I[HTTP 500]
    H --> J[Send Confirmation Email]
    J --> K[Return Order Details]
    K --> L[End]
    E --> M[Get Order]
    M --> N{Order Found?}
    N -- Yes --> O[Check Authorization]
    O -- No --> P[HTTP 403]
    O -- Yes --> Q[Return Order Details]
    Q --> L
    M --> R{Order Status?}
    R -- Pending --> S[Return Order Details]
    R -- Not Pending --> T[HTTP 400]
    S --> L
    L --> U[List Orders]
    U --> V{Valid Parameters?}
    V -- Yes --> W[Fetch Orders]
    V -- No --> X[HTTP 400]
    W --> Y[Return Orders]
    Y --> L
    U --> Z[Cancel Order]
    Z --> AA{Order Found?}
    AA -- Yes --> AB[Check Authorization]
    AB -- No --> AC[HTTP 403]
    AB -- Yes --> AD[Check Order Status]
    AD -- Pending --> AE[Cancel Order]
    AD -- Not Pending --> AF[HTTP 400]
    AE --> L
```

## Dependencies

- `verify_token`: Verifies the JWT token for authentication.
- `send_order_confirmation`: Sends a confirmation email to the user after order creation.
- `OrderRepository`: Manages the database operations for orders.
- `get_current_user`: Dependency for getting the current authenticated user.

## Payment Processing

The payment processing is handled by the `PaymentProcessor` class in the `payments/processor.py` module. It supports multiple payment providers and transaction management.

```python
class PaymentProcessor:
    def __init__(self, provider: PaymentProvider = PaymentProvider.STRIPE):
        self.provider = provider
```

## Notes

- All endpoints require authentication via JWT token.
- Only the order owner can access or modify their orders.
- Pending orders can be cancelled, while processing or shipped orders cannot.

```

This Markdown document provides a comprehensive overview of the Order API endpoints, including their descriptions, request/response formats, and error handling. It also includes a flowchart illustrating the logic flow of the endpoints and a section on dependencies and payment processing.