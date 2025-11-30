# E-commerce Microservices (Flask + Docker Compose)

This project contains a minimal microservice-based e-commerce API composed of four Flask services:

- **product_service** — CRUD for products (`/products`)
- **user_service** — CRUD for users (`/users`)
- **orders_service** — CRUD for orders + items (`/orders`)
- **reviews_service** — CRUD for reviews (`/reviews`)

Each service uses SQLite (persisted in a Docker volume) via SQLAlchemy and exposes a simple REST API with JSON responses and a `/health` endpoint.

## Quick start

```bash
docker compose up --build
```

The services will be available at:

- http://localhost:5001 (products)
- http://localhost:5002 (users)
- http://localhost:5003 (orders)  
- http://localhost:5004 (reviews)

## Example requests

Create a product:

```bash
curl -X POST http://localhost:5001/products -H "Content-Type: application/json" -d '{"name":"T-shirt","description":"Cotton","price":19.99,"stock":100}'
```

List products:

```bash
curl http://localhost:5001/products
```

Create a user:

```bash
curl -X POST http://localhost:5002/users -H "Content-Type: application/json" -d '{"name":"nigan","email":"nigan@example.com"}'
```

Create an order:

```bash
curl -X POST http://localhost:5003/orders -H "Content-Type: application/json" -d '{
  "user_id": 1,
  "items": [
    {"product_id": 1, "quantity": 2, "price": 19.99},
    {"product_id": 2, "quantity": 1, "price": 49.99}
  ]
}'
```

Create a review:

```bash
curl -X POST http://localhost:5004/reviews -H "Content-Type: application/json" -d '{
  "product_id": 1,
  "user_id": 1,
  "rating": 5,
  "comment": "Great quality!"
}'
```

> Note: For simplicity, cross-service validation (e.g., verifying `user_id` or `product_id` exists) is not enforced. In a production system we might add service-to-service calls, messaging, and proper auth.
