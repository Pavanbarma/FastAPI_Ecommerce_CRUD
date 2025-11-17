from fastapi import FastAPI
from database import engine, Base
from routers import users, products, orders

# Create database tables
Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI(
    title="E-Commerce API",
    description="A REST API for E-Commerce platform with CRUD operations",
    version="1.0.0"
)

# Include routers
app.include_router(users.router)
app.include_router(products.router)
app.include_router(orders.router)


@app.get("/")
def root():
    return {
        "message": "Welcome to E-Commerce API",
        "docs": "/docs",
        "version": "1.0.0"
    }

