from pydantic import BaseModel, EmailStr
from datetime import date
from typing import Optional, List
from enum import Enum

# Enums
class CategoryType(str, Enum):
    COW = "cow"
    BUFFALO = "buffalo"
    GHEE = "ghee"

class ProductSize(str, Enum):
    HALF_LITER = "0.5 lit"
    ONE_LITER = "1 lit"
    TWO_LITER = "2 lit"

# --- User Schemas ---
class UserBase(BaseModel):
    username: str
    email: EmailStr
    is_active: bool = True

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int

    class Config:
        orm_mode = True

# --- Customer Schemas ---
class CustomerBase(BaseModel):
    name: str
    phone: str
    address: Optional[str] = None

class CustomerCreate(CustomerBase):
    pass

class Customer(CustomerBase):
    id: int

    class Config:
        orm_mode = True

# --- Product Schemas ---
class ProductBase(BaseModel):
    category: CategoryType
    size: ProductSize
    price: float = 0.0

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int

    class Config:
        orm_mode = True

# --- Subscription Schemas ---
class SubscriptionBase(BaseModel):
    start_date: date
    end_date: date
    category: CategoryType
    product_id: Optional[int] = None
    customer_id: Optional[int] = None

class SubscriptionCreate(SubscriptionBase):
    pass

class Subscription(SubscriptionBase):
    id: int
    product: Optional[Product] = None
    customer: Optional[Customer] = None

    class Config:
        orm_mode = True
