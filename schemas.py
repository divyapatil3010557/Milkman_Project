from pydantic import BaseModel
from typing import Optional, List
from datetime import date
from enum import Enum

class ProductSize(str, Enum):
    HALF_LITER = "0.5 lit"
    ONE_LITER = "1 lit"
    TWO_LITER = "2 lit"

# --- User ---
class UserBase(BaseModel):
    username: str
    email: str
    is_active: bool = True

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    class Config:
        from_attributes = True

# --- Category ---
class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    id: int
    class Config:
        from_attributes = True

# --- Product ---
class ProductBase(BaseModel):
    size: ProductSize
    price: float
    category_id: int

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int
    category: Optional[Category] = None
    class Config:
        from_attributes = True

# --- Customer ---
class CustomerBase(BaseModel):
    name: str
    phone: str
    address: Optional[str] = None

class CustomerCreate(CustomerBase):
    pass

class Customer(CustomerBase):
    id: int
    class Config:
        from_attributes = True

# --- Subscription ---
class SubscriptionBase(BaseModel):
    start_date: date
    end_date: date
    category_id: int
    product_id: Optional[int] = None
    customer_id: int

class SubscriptionCreate(SubscriptionBase):
    pass

class Subscription(SubscriptionBase):
    id: int
    category: Optional[Category] = None
    product: Optional[Product] = None
    customer: Optional[Customer] = None
    class Config:
        from_attributes = True
