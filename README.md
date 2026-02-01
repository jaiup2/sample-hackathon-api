# Sample E-Commerce API

A demo repository for the Living Repository Sentinel hackathon project.

## Project Structure

```
sample_repo/
├── README.md           # This file
├── src/
│   ├── auth/           # Authentication module
│   ├── api/            # REST API endpoints
│   ├── database/       # Database connectors
│   └── utils/          # Utility functions
├── tests/              # Test files
└── docs/               # Documentation
```

## Quick Start

1. Install dependencies: `pip install -r requirements.txt`
2. Set up environment variables (see `.env.example`)
3. Run migrations: `python -m src.database.migrate`
4. Start server: `python -m src.main`

## Architecture Decisions

### Why OAuth2 instead of SAML? (PR #42)

We chose OAuth2 for our authentication layer because:
- Better mobile support for our upcoming mobile app
- Simpler integration with third-party services
- More widely adopted standard in 2025

### Database Choice: PostgreSQL with Redis Cache

- PostgreSQL for persistent data (users, orders, products)
- Redis for session management and caching
- This hybrid approach gives us both reliability and speed

## Key Flows

### User Authentication Flow
1. User submits credentials to `/api/auth/login`
2. `auth/login.py` validates credentials against database
3. If valid, generates JWT token using `auth/tokens.py`
4. Token returned to client, stored in Redis for session tracking

### Order Processing Flow
1. Request hits `/api/orders/create`
2. `api/orders.py` validates order data
3. `database/orders.py` persists order
4. `utils/notifications.py` sends confirmation email
# Test trigger for webhook
