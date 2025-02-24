import re
from datetime import date

from fastapi.exceptions import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Query, Session

from src import models, schemas


def create_unique_constrain_error_msg(exc: IntegrityError) -> str | None:
    pattern = r"^UNIQUE constraint failed: ([a-z_]+)\.([a-z_]+)$"
    args = exc.orig and exc.orig.args
    args = args or tuple()
    for arg in args:
        assert isinstance(arg, str)
        match = re.match(pattern, arg)
        if match:
            table, column = match.groups()
            singular = table[:-3] + "y" if table.endswith("ies") else table[:-1]
            record = singular.replace("_", " ")
            return f"A {record} already exists with that {column}"
    return None


# User


def read_user(db: Session, username: str) -> models.User | None:
    return db.query(models.User).filter(models.User.name == username).first()


# Customer


def create_customer(db: Session, customer: schemas.CustomerCreate) -> models.Customer:
    db_customer = models.Customer(**customer.dict())
    db.add(db_customer)
    db.commit()
    return db_customer


def read_customer(db: Session, customer_id: int) -> models.Customer | None:
    return db.query(models.Customer).filter(models.Customer.id == customer_id).first()


def read_customers(
    db: Session,
    name: str | None,
    email: str | None,
    phone: str | None,
    order_by: str,
    descending: bool,
) -> Query[models.Customer]:
    query = db.query(models.Customer)
    if name is not None:
        query = query.filter(models.Customer.name.startswith(name.lower()))
    if email is not None:
        query = query.filter(models.Customer.email.startswith(email.lower()))
    if phone is not None:
        query = query.filter(models.Customer.phone.startswith(phone.lower()))

    if order_by == "name":
        order_by_field = models.Customer.name
    elif order_by == "email":
        order_by_field = models.Customer.email
    elif order_by == "phone":
        order_by_field = models.Customer.phone
    else:
        raise ValueError(order_by)
    if descending:
        return query.order_by(order_by_field.desc())
    return query.order_by(order_by_field)


def update_customer(
    db: Session, customer_id: int, customer: schemas.CustomerEdit
) -> models.Customer:
    db_customer = db.query(models.Customer).filter(models.Customer.id == customer_id).first()
    if db_customer is None:
        raise HTTPException(404, "Customer not found")
    for attr, value in customer.dict(exclude={"id"}, exclude_unset=True).items():
        setattr(db_customer, attr, value)
    db.add(db_customer)
    db.commit()
    return db_customer


# MenuCategory


def create_menu_category(db: Session, category: schemas.MenuCategoryCreate) -> models.MenuCategory:
    db_category = models.MenuCategory(**category.dict())
    db.add(db_category)
    db.commit()
    return db_category


def read_menu_category(db: Session, category_id: int) -> models.MenuCategory | None:
    return db.query(models.MenuCategory).filter(models.MenuCategory.id == category_id).first()


def read_menu_categories(db: Session):
    return db.query(models.MenuCategory)


def update_menu_category(
    db: Session, category_id: int, category: schemas.MenuCategoryEdit
) -> models.MenuCategory:
    db_category = (
        db.query(models.MenuCategory).filter(models.MenuCategory.id == category_id).first()
    )
    if db_category is None:
        raise HTTPException(404, "Menu category not found")
    for attr, value in category.dict(exclude={"id"}, exclude_unset=True).items():
        setattr(db_category, attr, value)
    db.add(db_category)
    db.commit()
    return db_category


# MenuItem


def create_menu_item(db: Session, menu_item: schemas.MenuItemCreate) -> models.MenuItem:
    db_menu_item = models.MenuItem(**menu_item.dict())
    db.add(db_menu_item)
    db.commit()
    return db_menu_item


def read_menu_item(db: Session, menu_item_id: int) -> models.MenuItem | None:
    return db.query(models.MenuItem).filter(models.MenuItem.id == menu_item_id).first()


def read_menu_items(
    db: Session, category_id: int | None, name: str | None, descending: bool
) -> Query[models.MenuItem]:
    query = db.query(models.MenuItem)
    if category_id is not None:
        query = query.filter(models.MenuItem.category_id == category_id)
    if name is not None:
        query = query.filter(models.MenuItem.name.startswith(name))
    order_by = models.MenuItem.name.desc() if descending else models.MenuItem.name
    return query.order_by(order_by)


def update_menu_item(
    db: Session, menu_item_id: int, menu_item: schemas.MenuItemEdit
) -> models.MenuItem:
    db_menu_item = db.query(models.MenuItem).filter(models.MenuItem.id == menu_item_id).first()
    if db_menu_item is None:
        raise HTTPException(404, "Menu item not found")
    for attr, value in menu_item.dict(exclude={"id"}, exclude_unset=True).items():
        setattr(db_menu_item, attr, value)
    db.add(db_menu_item)
    db.commit()
    return db_menu_item


# Campaign


def create_campaign(db: Session, campaign: schemas.CampaignCreate) -> models.Campaign:
    db_campaign = models.Campaign(**campaign.dict())
    db.add(db_campaign)
    db.commit()
    return db_campaign


def read_campaign(db: Session, campaign_id: int) -> models.Campaign | None:
    return db.query(models.Campaign).filter(models.Campaign.id == campaign_id).first()


def read_campaigns(db: Session) -> Query[models.Campaign]:
    return db.query(models.Campaign)


def update_campaign(
    db: Session, campaign_id: int, campaign: schemas.CampaignEdit
) -> models.Campaign:
    db_campaign = db.query(models.Campaign).filter(models.Campaign.id == campaign_id).first()
    if db_campaign is None:
        raise HTTPException(404, "Campaign not found")
    for attr, value in campaign.dict(exclude={"id"}, exclude_unset=True).items():
        setattr(db_campaign, attr, value)
    db.add(db_campaign)
    db.commit()
    return db_campaign


# Payments


def create_payment(db: Session, payment: schemas.PaymentCreate) -> models.Order:
    db_payment = models.Payment(**payment.dict())
    db.add(db_payment)
    db.commit()
    return db_payment.order


def read_payment(db: Session, payment_id: int) -> models.Payment | None:
    return db.query(models.Payment).filter(models.Payment.id == payment_id).first()


def read_payments(
    db: Session,
    inclusive_start_date: date | None,
    exclusive_end_date: date | None,
) -> Query[models.Payment]:
    query = db.query(models.Payment)
    if inclusive_start_date is not None:
        query = query.filter(models.Payment.date >= inclusive_start_date)
    if exclusive_end_date is not None:
        query = query.filter(models.Payment.date < exclusive_end_date)
    return query


def update_payment(db: Session, payment_id: int, payment: schemas.PaymentEdit) -> models.Order:
    db_payment = db.query(models.Payment).filter(models.Payment.id == payment_id).first()
    if db_payment is None:
        raise HTTPException(404, "Payment not found")
    if db_payment.order_id != payment.order_id:
        raise HTTPException(400, "Invalid payment id")

    d = payment.dict(exclude={"id", "order_id"}, exclude_unset=True)
    for attr, value in d.items():
        setattr(db_payment, attr, value)
    db.add(db_payment)
    db.commit()
    return db_payment.order


def delete_payment(db: Session, payment_id: int) -> models.Order:
    db_payment = db.query(models.Payment).filter(models.Payment.id == payment_id).first()
    if db_payment is None:
        raise HTTPException(404, "Payment not found")
    db.delete(db_payment)
    db.commit()
    return db.query(models.Order).filter(models.Order.id == db_payment.order_id).one()


# OrderItem


def read_order_item(db: Session, order_item_id: int) -> models.OrderItem | None:
    return db.query(models.OrderItem).filter(models.OrderItem.id == order_item_id).one_or_none()


def create_order_item(db: Session, order_item: schemas.OrderItemCreate) -> models.Order:
    db_order_item = models.OrderItem(**order_item.dict())
    db.add(db_order_item)
    db.commit()
    return db_order_item.order


def update_order_item(
    db: Session, order_item_id: int, order_item: schemas.OrderItemEdit
) -> models.Order:
    db_order_item = db.query(models.OrderItem).filter(models.OrderItem.id == order_item_id).first()
    if db_order_item is None:
        raise HTTPException(404, "Order item not found")
    if db_order_item.order_id != order_item.order_id:
        raise HTTPException(400, "Invalid order id")
    d = order_item.dict(exclude={"id", "order_id"}, exclude_unset=True)
    for attr, value in d.items():
        setattr(db_order_item, attr, value)
    db.add(db_order_item)
    db.commit()
    return db_order_item.order


def delete_order_item(db: Session, order_item_id: int) -> models.Order:
    db_order_item = db.query(models.OrderItem).filter(models.OrderItem.id == order_item_id).first()
    if db_order_item is None:
        raise HTTPException(404, detail="Order item not found")
    db.delete(db_order_item)
    db.commit()
    return db.query(models.Order).filter(models.Order.id == db_order_item.order_id).one()


# Order


def create_order(db: Session, order: schemas.OrderCreate) -> models.Order:
    if len(order.order_items) == 0:
        raise HTTPException(400, detail="An order requires at least 1 item")

    db_order = models.Order(**order.dict(exclude={"order_items", "payments"}))
    db.add(db_order)
    db.commit()

    for order_item in order.order_items:
        db_order_item = models.OrderItem(**order_item.dict(), order_id=db_order.id)
        db.add(db_order_item)

    for payment in order.payments:
        db_payment = models.Payment(**payment.dict(), order_id=db_order.id)
        db.add(db_payment)

    db.commit()
    return db_order


def read_order(db: Session, order_id: int) -> models.Order | None:
    return db.query(models.Order).filter(models.Order.id == order_id).first()


def read_orders(db: Session, completed: bool) -> Query[models.Order]:
    return db.query(models.Order).filter(models.Order.completed == completed)


def update_order(db: Session, order_id: int, order: schemas.OrderEdit) -> models.Order:
    db_order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if db_order is None:
        raise HTTPException(404, "Order not found")
    for attr, value in order.dict(exclude={"id"}, exclude_unset=True).items():
        setattr(db_order, attr, value)
    db.add(db_order)
    db.commit()
    return db_order


def delete_order(db: Session, order_id: int) -> bool:
    db_order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if db_order is None:
        raise HTTPException(404, "Order not found")
    for db_order_item in db_order.order_items:
        db.delete(db_order_item)
    for db_payment in db_order.payments:
        db.delete(db_payment)
    db.delete(db_order)
    db.commit()
    return True
