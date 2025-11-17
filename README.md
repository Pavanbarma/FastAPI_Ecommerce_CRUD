# FastAPI E-Commerce CRUD API

A complete REST API for an e-commerce platform built with FastAPI, PostgreSQL, and SQLAlchemy. This project provides full CRUD (Create, Read, Update, Delete) operations for Users, Products, and Orders.

## Features

- ✅ RESTful API with FastAPI
- ✅ PostgreSQL database integration
- ✅ SQLAlchemy ORM for database operations
- ✅ Pydantic models for data validation
- ✅ Complete CRUD operations for:
  - Users
  - Products
  - Orders
- ✅ Automatic API documentation (Swagger UI)
- ✅ Database schema with relationships
- ✅ Sample data included

## Project Structure

```
FastAPI_CRUD/
├── main.py              # FastAPI application entry point
├── database.py          # Database connection and session management
├── models.py            # SQLAlchemy database models
├── schemas.py           # Pydantic schemas for request/response validation
├── crud.py              # CRUD operations for all entities
├── schema.sql           # SQL schema file for database setup
├── requirements.txt     # Python dependencies
├── .env.example         # Environment variables template
├── .gitignore          # Git ignore file
└── routers/            # API route handlers
    ├── __init__.py
    ├── users.py        # User endpoints
    ├── products.py     # Product endpoints
    └── orders.py       # Order endpoints
```

## Prerequisites

Before you begin, ensure you have the following installed:

- Python 3.8 or higher
- PostgreSQL 12 or higher
- pip (Python package manager)

## Setup Instructions

### Step 1: Clone or Navigate to Project Directory

```bash
cd FastAPI_CRUD
```

### Step 2: Create Virtual Environment (Recommended)

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Set Up PostgreSQL Database

1. **Install PostgreSQL** (if not already installed)
   - Download from: https://www.postgresql.org/download/
   - During installation, remember your PostgreSQL password

2. **Create Database**

   Open PostgreSQL command line (psql) or pgAdmin and run:

   ```sql
   CREATE DATABASE ecommerce_db;
   ```

   Or using command line:
   ```bash
   psql -U postgres
   CREATE DATABASE ecommerce_db;
   \q
   ```

3. **Run SQL Schema**

   Option 1: Using psql command line:
   ```bash
   psql -U postgres -d ecommerce_db -f schema.sql
   ```

   Option 2: Using pgAdmin:
   - Open pgAdmin
   - Connect to your PostgreSQL server
   - Right-click on `ecommerce_db` → Query Tool
   - Open and execute `schema.sql` file

### Step 5: Configure Environment Variables

1. Create a `.env` file in the project root:

   ```bash
   cp .env.example .env
   ```

2. Edit `.env` file with your database credentials:

   ```
   DATABASE_URL=postgresql://username:password@localhost:5432/ecommerce_db
   ```

   Replace:
   - `username`: Your PostgreSQL username (default: `postgres`)
   - `password`: Your PostgreSQL password
   - `localhost:5432`: Your PostgreSQL host and port
   - `ecommerce_db`: Your database name

   Example:
   ```
   DATABASE_URL=postgresql://postgres:mypassword@localhost:5432/ecommerce_db
   ```

### Step 6: Run the Application

```bash
uvicorn main:app --reload
```

The API will be available at:
- **API**: http://localhost:8000
- **Interactive API Docs (Swagger UI)**: http://localhost:8000/docs
- **Alternative API Docs (ReDoc)**: http://localhost:8000/redoc

## API Endpoints

### Users

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/users/` | Create a new user |
| GET | `/users/` | Get all users (with pagination) |
| GET | `/users/{user_id}` | Get user by ID |
| PUT | `/users/{user_id}` | Update user |
| DELETE | `/users/{user_id}` | Delete user |

### Products

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/products/` | Create a new product |
| GET | `/products/` | Get all products (with pagination) |
| GET | `/products/{product_id}` | Get product by ID |
| PUT | `/products/{product_id}` | Update product |
| DELETE | `/products/{product_id}` | Delete product |

### Orders

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/orders/` | Create a new order |
| GET | `/orders/` | Get all orders (with pagination) |
| GET | `/orders/{order_id}` | Get order by ID |
| GET | `/orders/user/{user_id}` | Get orders by user ID |
| PUT | `/orders/{order_id}` | Update order status |
| DELETE | `/orders/{order_id}` | Delete order |

## Example API Requests

### Create a User

```bash
POST http://localhost:8000/users/
Content-Type: application/json

{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "securepassword123"
}
```

### Create a Product

```bash
POST http://localhost:8000/products/
Content-Type: application/json

{
  "name": "Laptop",
  "description": "High-performance laptop",
  "price": 999.99,
  "stock": 50
}
```

### Create an Order

```bash
POST http://localhost:8000/orders/
Content-Type: application/json

{
  "user_id": 1,
  "order_items": [
    {
      "product_id": 1,
      "quantity": 2,
      "price": 999.99
    },
    {
      "product_id": 2,
      "quantity": 1,
      "price": 699.99
    }
  ]
}
```

### Get All Products

```bash
GET http://localhost:8000/products/?skip=0&limit=10
```

## Database Schema

The database consists of 4 main tables:

1. **users**: Stores user information
   - id, name, email, password, created_at

2. **products**: Stores product information
   - id, name, description, price, stock, created_at

3. **orders**: Stores order information
   - id, user_id, total_amount, status, created_at

4. **order_items**: Stores order line items
   - id, order_id, product_id, quantity, price

Relationships:
- Users → Orders (One-to-Many)
- Orders → Order Items (One-to-Many)
- Products → Order Items (One-to-Many)

## Testing the API

### Using Swagger UI (Recommended)

1. Navigate to http://localhost:8000/docs
2. Click on any endpoint to expand it
3. Click "Try it out"
4. Fill in the required parameters
5. Click "Execute"

### Using cURL

```bash
# Get all products
curl http://localhost:8000/products/

# Create a product
curl -X POST http://localhost:8000/products/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Test Product", "price": 99.99, "stock": 10}'
```

### Using Python requests

```python
import requests

# Get all products
response = requests.get("http://localhost:8000/products/")
print(response.json())

# Create a product
data = {
    "name": "Test Product",
    "price": 99.99,
    "stock": 10
}
response = requests.post("http://localhost:8000/products/", json=data)
print(response.json())
```

## Troubleshooting

### Database Connection Error

- Verify PostgreSQL is running
- Check database credentials in `.env` file
- Ensure database `ecommerce_db` exists
- Verify PostgreSQL port (default: 5432)

### Module Not Found Error

- Ensure virtual environment is activated
- Run `pip install -r requirements.txt` again

### Port Already in Use

- Change the port: `uvicorn main:app --reload --port 8001`
- Or stop the process using port 8000

## Next Steps

- Add authentication and authorization (JWT tokens)
- Implement password hashing
- Add input validation and error handling
- Add unit tests
- Add logging
- Deploy to production (Docker, cloud platforms)

## License

This project is open source and available for educational purposes.
