from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import crud, schemas
from ..database import get_db

router = APIRouter(
    prefix="/subscriptions",
    tags=["subscriptions"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=schemas.Subscription)
def create_subscription(subscription: schemas.SubscriptionCreate, db: Session = Depends(get_db)):
    # Validate Category
    category = crud.get_category(db, category_id=subscription.category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    # Validate Customer
    customer = crud.get_customer(db, customer_id=subscription.customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    # Validate Product if provided
    if subscription.product_id:
        product = crud.get_product(db, product_id=subscription.product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        # Ensure product belongs to the category
        if product.category_id != subscription.category_id:
            raise HTTPException(status_code=400, detail="Product does not belong to the selected category")
    
    return crud.create_subscription(db=db, subscription=subscription)

@router.get("/", response_model=List[schemas.Subscription])
def read_subscriptions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_subscriptions(db, skip=skip, limit=limit)

@router.get("/{subscription_id}", response_model=schemas.Subscription)
def read_subscription(subscription_id: int, db: Session = Depends(get_db)):
    db_subscription = crud.get_subscription(db, subscription_id=subscription_id)
    if db_subscription is None:
        raise HTTPException(status_code=404, detail="Subscription not found")
    return db_subscription
