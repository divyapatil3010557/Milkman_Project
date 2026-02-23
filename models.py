from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey, Enum, Boolean
from sqlalchemy.orm import relationship
import enum
from .database import Base

class CategoryType(str, enum.Enum):
    COW = "cow"
    BUFFALO = "buffalo"
    GHEE = "ghee"

class ProductSize(str, enum.Enum):
    HALF_LITER = "0.5 lit"
    ONE_LITER = "1 lit"
    TWO_LITER = "2 lit"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    is_active = Column(Boolean, default=True)

class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    phone = Column(String, unique=True, index=True)
    address = Column(String)
    
    subscriptions = relationship("Subscription", back_populates="customer")

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    category = Column(Enum(CategoryType), nullable=False)
    size = Column(Enum(ProductSize), nullable=False)
    price = Column(Float, default=0.0)

    subscriptions = relationship("Subscription", back_populates="product")

class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True, index=True)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    category = Column(Enum(CategoryType), nullable=False)
    
    product_id = Column(Integer, ForeignKey("products.id"), nullable=True)
    product = relationship("Product", back_populates="subscriptions")
    
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=True)
    customer = relationship("Customer", back_populates="subscriptions")
