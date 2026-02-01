

[Constraints]:
1. Do not include any code snippets or references to the source code.
2. Focus on documenting the API endpoints, their expected inputs, outputs, and any dependencies.
3. Include information about authentication and authorization.
4. Mention any external library dependencies.
5. Use clear and concise language.

# API Documentation: Order Management

This documentation outlines the REST API endpoints for managing orders in the e-commerce application. All endpoints require authentication via JWT token.

## Endpoints

### 1. Create a new order

**Endpoint:** `/api/orders/create`

**Method:** `POST`

**Description:** This endpoint creates a new order. It validates the order items, calculates the total price, processes payment (placeholder), creates the order record, and sends a confirmation email.

**Request Body:**

| Name          | Type    | Description                                                                 |
|---------------|---------|-----------------------------------------------------------------------------|
| items         | list    | List of `OrderItem` objects containing product details and quantities.     |
| shipping_address | str    | The shipping address for the order.                                       |
| payment_method | str    | The payment method for the order.                                         |

**Authentication:** JWT token required.

**Response:**

| Name          | Type    | Description                                                                 |
|---------------|---------|-----------------------------------------------------------------------------|
| order_id      | str     | The unique identifier for the created order.                               |
| status        | str     | The current status of the order (e.g., 'pending', 'processing', 'completed').|
| total         | float   | The total price of the order.                                               |
| items         | list    | List of `OrderItem` objects representing the order items.                   |
| created_at    | str     | The timestamp when the order was created.                                   |

**Error Handling:**

- `HTTPException` with status code `400` if validation fails.
- `HTTPException` with status code `500` if payment processing fails.

### 2. Get order details

**Endpoint:** `/api/orders/{order_id}`

**Method:** `GET`

**Description:** This endpoint retrieves the details of a specific order by its ID. Users can only access their own orders.

**Path Parameters:**

| Name          | Type    | Description                                                                 |
|---------------|---------|-----------------------------------------------------------------------------|
| order_id      | str     | The unique identifier for the order.                                       |

**Authentication:** JWT token required.

**Response:**

| Name          | Type    | Description                                                                 |
|---------------|---------|-----------------------------------------------------------------------------|
| order_id      | str     | The unique identifier for the order.                                       |
| status        | str     | The current status of the order (e.g., 'pending', 'processing', 'completed').|
| total         | float   | The total price of the order.                                               |
| items         | list    | List of `OrderItem` objects representing the order items.                   |
| created_at    | str     | The timestamp when the order was created.                                   |

**Error Handling:**

- `HTTPException` with status code `404` if the order is not found.
- `HTTPException` with status code `403` if the user is not authorized to access the order.

### 3. List user orders

**Endpoint:** `/api/orders/`

**Method:** `GET`

**Description:** This endpoint lists all orders for the current user, supporting pagination via `limit` and `offset` parameters.

**Query Parameters:**

| Name          | Type    | Description                                                                 |
|---------------|---------|-----------------------------------------------------------------------------|
| limit         | int     | The maximum number of orders to return.                                     |
| offset        | int     | The number of orders to skip before starting to collect the result set.    |

**Authentication:** JWT token required.

**Response:**

| Name          | Type    | Description                                                                 |
|---------------|---------|-----------------------------------------------------------------------------|
| order_id      | str     | The unique identifier for the order.                                       |
| status        | str     | The current status of the order (e.g., 'pending', 'processing', 'completed').|
| total         | float   | The total price of the order.                                               |
| items         | list    | List of `OrderItem` objects representing the order items.                   |
| created_at    | str     | The timestamp when the order was created.                                   |

**Error Handling:**

- `HTTPException` with status code `401` if the user is not authenticated.

### 4. Cancel an order

**Endpoint:** `/api/orders/{order_id}/cancel`

**Method:** `POST`

**Description:** This endpoint cancels a pending order. Only pending orders can be cancelled.

**Path Parameters:**

| Name          | Type    | Description                                                                 |
|---------------|---------|-----------------------------------------------------------------------------|
| order_id      | str     | The unique identifier for the order.                                       |

**Authentication:** JWT token required.

**Response:**

| Name          | Type    | Description                                                                 |
|---------------|---------|-----------------------------------------------------------------------------|
| message       | str     | A confirmation message indicating the order was cancelled successfully.     |

**Error Handling:**

- `HTTPException` with status code `404` if the order is not found.
- `HTTPException` with status code `403` if the user is not authorized to cancel the order.
- `HTTPException` with status code `400` if the order status is not 'pending'.

## External Dependencies

- **FastAPI**: A modern, fast (high-performance), web framework for building APIs with Python 3.6+ based on standard Python type hints.
- **Pydantic**: A data validation library for Python, based on type hints.
- **SQLAlchemy**: A SQL toolkit and Object-Relational Mapping (ORM) system for Python, providing a full suite of well-known enterprise-level persistence patterns.
- **OAuth2**: A library for handling OAuth2 authentication and authorization.
- **Stripe**: A payment processing platform.
- **PayPal**: A payment processing platform.
- **Square**: A payment processing platform.

## Authentication and Authorization

All endpoints require authentication via JWT token. The `get_current_user` function is used to retrieve the current authenticated user from the token. If the token is invalid or expired, an `HTTPException` with status code `401` is raised.

For authorization, the current user's ID is compared with the order's user ID to ensure the user can only access their own orders. If the user is not authorized, an `HTTPException` with status code `403` is raised.