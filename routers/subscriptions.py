from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import crud, schemas, database

router = APIRouter(
    prefix="/subscriptions",
    tags=["subscriptions"],
    responses={404: {"description": "Not found"}},
)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.Subscription)
def create_subscription(subscription: schemas.SubscriptionCreate, db: Session = Depends(get_db)):
    # Validate product exists
    product = crud.get_product(db, product_id=subscription.product_id)
    if not product and subscription.product_id:
         raise HTTPException(status_code=404, detail="Product not found")
    
    # Validate customer exists
    if subscription.customer_id:
        customer = crud.get_customer(db, customer_id=subscription.customer_id)
        if not customer:
             raise HTTPException(status_code=404, detail="Customer not found")

    return crud.create_subscription(db=db, subscription=subscription)

@router.get("/", response_model=list[schemas.Subscription])
def read_subscriptions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    subscriptions = crud.get_subscriptions(db, skip=skip, limit=limit)
    return subscriptions

@router.get("/{subscription_id}", response_model=schemas.Subscription)
def read_subscription(subscription_id: int, db: Session = Depends(get_db)):
    db_subscription = crud.get_subscription(db, subscription_id=subscription_id)
    if db_subscription is None:
        raise HTTPException(status_code=404, detail="Subscription not found")
    return db_subscription
