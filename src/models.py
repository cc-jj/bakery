from datetime import datetime, timezone

from sqlalchemy import (
    Boolean,
    Column,
    Date,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    TypeDecorator,
)
from sqlalchemy.orm import DeclarativeBase, relationship


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


class DateTimeUTC(TypeDecorator):
    impl = DateTime

    def process_bind_param(self, value, dialect):
        assert isinstance(value, datetime)
        assert datetime.tzinfo is not None
        return value

    def process_result_value(self, value, dialect):
        assert isinstance(value, datetime)
        assert value.tzinfo is None
        return value.replace(tzinfo=timezone.utc)


class Base(DeclarativeBase):
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    date_created = Column(DateTimeUTC, default=utcnow, nullable=False)
    date_modified = Column(DateTimeUTC, default=utcnow, onupdate=utcnow, nullable=False)


class User(Base):
    __tablename__ = "users"
    name = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)


class Customer(Base):
    __tablename__ = "customers"
    name = Column(String, index=True, nullable=False)
    email = Column(String, unique=True, index=True)
    phone = Column(String, unique=True, index=True)
    notes = Column(String)

    orders = relationship("Order", back_populates="customer")


class MenuItem(Base):
    __tablename__ = "menu_items"
    name = Column(String, index=True, nullable=False)
    category_id = Column(Integer, ForeignKey("menu_categories.id"), nullable=False)
    description = Column(String)
    price = Column(Float, nullable=False)
    price_units = Column(String)  # $10 / dozen <-- dozen is the unit

    order_items = relationship("OrderItem", back_populates="menu_item")
    category = relationship("MenuCategory", back_populates="menu_items")


class MenuCategory(Base):
    __tablename__ = "menu_categories"
    name = Column(String, unique=True, nullable=False)
    description = Column(String)

    menu_items = relationship("MenuItem", back_populates="category")


class OrderItem(Base):
    __tablename__ = "order_items"
    menu_item_id = Column(Integer, ForeignKey("menu_items.id"), nullable=False)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    quantity = Column(Float, nullable=False)
    menu_price = Column(Float, nullable=False)
    charged_price = Column(Float, nullable=False)
    notes = Column(String)

    order = relationship("Order", back_populates="order_items")
    menu_item = relationship("MenuItem", back_populates="order_items")


class Order(Base):
    __tablename__ = "orders"
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    campaign_id = Column(Integer, ForeignKey("campaigns.id"))
    date_ordered = Column(Date)
    date_delivered = Column(Date)
    price_adjustment = Column(Float)
    notes = Column(String)
    completed = Column(Boolean, default=False)

    campaign = relationship("Campaign", back_populates="orders")
    customer = relationship("Customer", back_populates="orders")
    order_items = relationship("OrderItem", back_populates="order")
    payments = relationship("Payment", back_populates="order")


class Campaign(Base):
    """Promotional campaigns, example Dec 18 2021 open house"""

    __tablename__ = "campaigns"
    name = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=False)
    date_start = Column(Date)
    date_end = Column(Date)

    orders = relationship("Order", back_populates="campaign")


class Payment(Base):
    __tablename__ = "payments"
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    amount = Column(Float, nullable=False)
    method = Column(String, nullable=False)  # cash, paypal, zelle
    date = Column(Date, nullable=False)

    order = relationship("Order", back_populates="payments")
