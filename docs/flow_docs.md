

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

- `verify_token`: A function to verify JWT tokens.
- `send_order_confirmation`: A function to send order confirmation emails.
- `OrderRepository`: A database repository for order management.
- `get_current_user`: A dependency for getting the current authenticated user.

## Payment Processing

The payment processing is handled by the `PaymentProcessor` class in the `payments/processor.py` module. It supports multiple payment providers and transaction management.

```
```

```json
{
  "endpoints": [
    {
      "name": "Create a New Order",
      "method": "POST",
      "path": "/api/orders/create",
      "description": "This endpoint allows users to create a new order by providing order items, shipping address, and payment method.",
      "request_body": {
        "items": [
          {
            "product_id": "string",
            "quantity": number,
            "price": number
          }
        ],
        "shipping_address": "string",
        "payment_method": "string"
      },
      "response": {
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
      },
      "error_handling": [
        {
          "code": 400,
          "description": "if validation fails"
        },
        {
          "code": 500,
          "description": "if payment processing fails"
        }
      ]
    },
    {
      "name": "Get Order Details",
      "method": "GET",
      "path": "/api/orders/{order_id}",
      "description": "This endpoint retrieves the details of a specific order by its ID. Users can only access their own orders.",
      "path_parameters": [
        {
          "name": "order_id",
          "type": "string",
          "description": "The unique identifier of the order."
        }
      ],
      "response": {
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
      },
      "error_handling": [
        {
          "code": 404,
          "description": "if the order is not found"
        },
        {
          "code": 403,
          "description": "if the user is not authorized to access the order"
        }
      ]
    },
    {
      "name": "List User Orders",
      "method": "GET",
      "path": "/api/orders/",
      "description": "This endpoint lists all orders for the current user, supporting pagination via `limit` and `offset` parameters.",
      "query_parameters": [
        {
          "name": "limit",
          "type": "integer",
          "default": 10,
          "description": "The number of orders to return per page."
        },
        {
          "name": "offset",
          "type": "integer",
          "default": 0,
          "description": "The number of orders to skip before starting to collect the result set."
        }
      ],
      "response": [
        {
          "order_id": "string",
          "status":