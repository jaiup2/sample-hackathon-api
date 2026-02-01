

[Constraints]:
1. Do not include any code snippets or references to the source code.
2. Focus on documenting the API endpoints, their expected inputs, outputs, and any external dependencies.
3. Include information about authentication and authorization.
4. Mention any error handling or exceptions that may be raised.

# API Documentation: Order Management

This documentation outlines the REST API endpoints for managing orders in the e-commerce application. All endpoints require authentication via JWT token.

## Endpoints

### 1. Create a new order

**Endpoint:** `/api/orders/create`

**Method:** `POST`

**Description:** This endpoint allows users to create a new order by providing order items, shipping address, and payment method.

**Request Body:**

| Field          | Type    | Description                                                                 |
|----------------|---------|-----------------------------------------------------------------------------|
| items          | List[OrderItem] | A list of order items, each containing `product_id`, `quantity`, and `price`. |
| shipping_address | str | The shipping address for the order. |
| payment_method | str | The payment method to be used for the order. |

**Authentication:** JWT token is required for authentication.

**Response:**

| Field          | Type    | Description                                                                 |
|----------------|---------|-----------------------------------------------------------------------------|
| order_id       | str     | The unique identifier for the created order. |
| status         | str     | The current status of the order (e.g., 'pending', 'processing', 'shipped'). |
| total          | float   | The total price of the order. |
| items          | List[OrderItem] | The list of order items. |
| created_at     | str     | The timestamp when the order was created. |

**Exceptions:**

- `HTTPException`: Raised if validation fails or payment processing fails.

### 2. Get order details

**Endpoint:** `/api/orders/{order_id}`

**Method:** `GET`

**Description:** This endpoint retrieves the details of a specific order by its ID. Users can only access their own orders.

**Path Parameters:**

| Field          | Type    | Description                                                                 |
|----------------|---------|-----------------------------------------------------------------------------|
| order_id       | str     | The unique identifier for the order. |

**Authentication:** JWT token is required for authentication.

**Response:**

| Field          | Type    | Description                                                                 |
|----------------|---------|-----------------------------------------------------------------------------|
| order_id       | str     | The unique identifier for the order. |
| status         | str     | The current status of the order (e.g., 'pending', 'processing', 'shipped'). |
| total          | float   | The total price of the order. |
| items          | List[OrderItem] | The list of order items. |
| created_at     | str     | The timestamp when the order was created. |

**Exceptions:**

- `HTTPException`: Raised if the order is not found or the user is not authorized to access the order.

### 3. List user orders

**Endpoint:** `/api/orders/`

**Method:** `GET`

**Description:** This endpoint lists all orders for the current user, supporting pagination via `limit` and `offset` parameters.

**Query Parameters:**

| Field          | Type    | Description                                                                 |
|----------------|---------|-----------------------------------------------------------------------------|
| limit          | int     | The number of orders to return per page. Default is 10. |
| offset         | int     | The number of orders to skip before starting to collect the result set. |

**Authentication:** JWT token is required for authentication.

**Response:**

| Field          | Type    | Description                                                                 |
|----------------|---------|-----------------------------------------------------------------------------|
| order_id       | str     | The unique identifier for the order. |
| status         | str     | The current status of the order (e.g., 'pending', 'processing', 'shipped'). |
| total          | float   | The total price of the order. |
| items          | List[OrderItem] | The list of order items. |
| created_at     | str     | The timestamp when the order was created. |

**Exceptions:**

- `HTTPException`: Raised if an error occurs during the retrieval of orders.

### 4. Cancel an order

**Endpoint:** `/api/orders/{order_id}/cancel`

**Method:** `POST`

**Description:** This endpoint allows users to cancel a pending order. Orders that are processing or shipped cannot be cancelled.

**Path Parameters:**

| Field          | Type    | Description                                                                 |
|----------------|---------|-----------------------------------------------------------------------------|
| order_id       | str     | The unique identifier for the order. |

**Authentication:** JWT token is required for authentication.

**Response:**

| Field          | Type    | Description                                                                 |
|----------------|---------|-----------------------------------------------------------------------------|
| message        | str     | A confirmation message indicating the order was cancelled successfully. |

**Exceptions:**

- `HTTPException`: Raised if the order is not found, the user is not authorized, or the order status is not 'pending'.

## External Dependencies

- **FastAPI**: A modern, fast (high-performance), web framework for building APIs with Python 3.6+ based on standard Python type hints.
- **Pydantic**: A data validation library for Python, based on type hints.
- **SQLAlchemy**: A SQL toolkit and Object-Relational Mapping (ORM) system for Python, providing a full suite of well-known enterprise-level persistence patterns.
- **OAuth2**: A standard protocol for authorization, used for securing APIs.
- **Stripe**, **PayPal**, **Square**: Payment processing providers supported by the application.

## Error Handling

- **HTTPException**: Raised for various error scenarios, including invalid or expired tokens, order not found, unauthorized access, and payment processing failures.

This documentation provides a comprehensive overview of the order management API endpoints, their expected inputs, outputs, and external dependencies. It also covers authentication, authorization, and error handling aspects.