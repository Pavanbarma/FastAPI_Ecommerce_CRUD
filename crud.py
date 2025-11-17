from sqlalchemy.orm import Session, joinedload
from sqlalchemy import desc
from models import User, Product, Order, OrderItem
from schemas import (
    UserCreate, ProductCreate, ProductUpdate,
    OrderCreate, OrderUpdate, OrderItemCreate
)


# User CRUD Operations
def create_user(db: Session, user: UserCreate):
    db_user = User(name=user.name, email=user.email, password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()


def update_user(db: Session, user_id: int, user_data: dict):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        for key, value in user_data.items():
            setattr(db_user, key, value)
        db.commit()
        db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user


# Product CRUD Operations
def create_product(db: Session, product: ProductCreate):
    db_product = Product(
        name=product.name,
        description=product.description,
        price=product.price,
        stock=product.stock
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def get_product(db: Session, product_id: int):
    return db.query(Product).filter(Product.id == product_id).first()


def get_products(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Product).order_by(desc(Product.created_at)).offset(skip).limit(limit).all()


def update_product(db: Session, product_id: int, product: ProductUpdate):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if db_product:
        update_data = product.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_product, key, value)
        db.commit()
        db.refresh(db_product)
    return db_product


def delete_product(db: Session, product_id: int):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
    return db_product


# Order CRUD Operations
def create_order(db: Session, order: OrderCreate):
    # Calculate total amount
    total_amount = sum(item.price * item.quantity for item in order.order_items)
    
    # Create order
    db_order = Order(
        user_id=order.user_id,
        total_amount=total_amount,
        status="pending"
    )
    db.add(db_order)
    db.flush()  # Flush to get order.id
    
    # Create order items
    for item in order.order_items:
        db_order_item = OrderItem(
            order_id=db_order.id,
            product_id=item.product_id,
            quantity=item.quantity,
            price=item.price
        )
        db.add(db_order_item)
    
    db.commit()
    db.refresh(db_order)
    return db_order


def get_order(db: Session, order_id: int):
    return db.query(Order).options(joinedload(Order.order_items)).filter(Order.id == order_id).first()


def get_orders(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Order).options(joinedload(Order.order_items)).order_by(desc(Order.created_at)).offset(skip).limit(limit).all()


def get_orders_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(Order).options(joinedload(Order.order_items)).filter(Order.user_id == user_id).order_by(desc(Order.created_at)).offset(skip).limit(limit).all()


def update_order(db: Session, order_id: int, order: OrderUpdate):
    db_order = db.query(Order).filter(Order.id == order_id).first()
    if db_order:
        update_data = order.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_order, key, value)
        db.commit()
        db.refresh(db_order)
    return db_order


def delete_order(db: Session, order_id: int):
    db_order = db.query(Order).filter(Order.id == order_id).first()
    if db_order:
        # Delete associated order items first
        db.query(OrderItem).filter(OrderItem.order_id == order_id).delete()
        db.delete(db_order)
        db.commit()
    return db_order

