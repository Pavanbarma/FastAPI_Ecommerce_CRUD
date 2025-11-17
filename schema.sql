-- E-Commerce Database Schema
-- PostgreSQL Database Schema for FastAPI CRUD Operations

-- Drop tables if they exist (in reverse order of dependencies)
DROP TABLE IF EXISTS order_items CASCADE;
DROP TABLE IF EXISTS orders CASCADE;
DROP TABLE IF EXISTS products CASCADE;
DROP TABLE IF EXISTS users CASCADE;

-- Create Users Table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create Index on email for faster lookups
CREATE INDEX idx_users_email ON users(email);

-- Create Products Table
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    stock INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create Orders Table
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    total_amount DECIMAL(10, 2) NOT NULL,
    status VARCHAR(50) DEFAULT 'pending',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Create Index on user_id for faster queries
CREATE INDEX idx_orders_user_id ON orders(user_id);

-- Create Order Items Table
CREATE TABLE order_items (
    id SERIAL PRIMARY KEY,
    order_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
);

-- Create Indexes for better query performance
CREATE INDEX idx_order_items_order_id ON order_items(order_id);
CREATE INDEX idx_order_items_product_id ON order_items(product_id);

-- Insert Sample Data (Optional)
-- Sample Users
INSERT INTO users (name, email, password) VALUES
('John Doe', 'john.doe@example.com', 'hashed_password_1'),
('Jane Smith', 'jane.smith@example.com', 'hashed_password_2'),
('Bob Johnson', 'bob.johnson@example.com', 'hashed_password_3');

-- Sample Products
INSERT INTO products (name, description, price, stock) VALUES
('Laptop', 'High-performance laptop with 16GB RAM', 999.99, 50),
('Smartphone', 'Latest smartphone with 128GB storage', 699.99, 100),
('Headphones', 'Wireless noise-cancelling headphones', 199.99, 75),
('Tablet', '10-inch tablet with stylus support', 449.99, 30),
('Smartwatch', 'Fitness tracking smartwatch', 299.99, 60);

-- Sample Orders
INSERT INTO orders (user_id, total_amount, status) VALUES
(1, 1699.98, 'completed'),
(2, 449.99, 'pending'),
(3, 499.98, 'processing');

-- Sample Order Items
INSERT INTO order_items (order_id, product_id, quantity, price) VALUES
(1, 1, 1, 999.99),
(1, 2, 1, 699.99),
(2, 4, 1, 449.99),
(3, 3, 2, 199.99),
(3, 5, 1, 299.99);

