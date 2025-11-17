from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from schemas import OrderCreate, OrderUpdate, OrderResponse
import crud

router = APIRouter(prefix="/orders", tags=["orders"])


@router.post("/", response_model=OrderResponse, status_code=201)
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    # Verify user exists
    db_user = crud.get_user(db, user_id=order.user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Verify products exist and get their prices
    for item in order.order_items:
        db_product = crud.get_product(db, product_id=item.product_id)
        if db_product is None:
            raise HTTPException(status_code=404, detail=f"Product {item.product_id} not found")
        # Use product price if not provided
        if item.price is None:
            item.price = db_product.price
    
    return crud.create_order(db=db, order=order)


@router.get("/", response_model=List[OrderResponse])
def read_orders(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    orders = crud.get_orders(db, skip=skip, limit=limit)
    return orders


@router.get("/user/{user_id}", response_model=List[OrderResponse])
def read_orders_by_user(user_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    orders = crud.get_orders_by_user(db, user_id=user_id, skip=skip, limit=limit)
    return orders


@router.get("/{order_id}", response_model=OrderResponse)
def read_order(order_id: int, db: Session = Depends(get_db)):
    db_order = crud.get_order(db, order_id=order_id)
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_order


@router.put("/{order_id}", response_model=OrderResponse)
def update_order(order_id: int, order: OrderUpdate, db: Session = Depends(get_db)):
    db_order = crud.update_order(db, order_id=order_id, order=order)
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_order


@router.delete("/{order_id}", status_code=204)
def delete_order(order_id: int, db: Session = Depends(get_db)):
    db_order = crud.delete_order(db, order_id=order_id)
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return None

