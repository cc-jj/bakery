import enum
from datetime import date, datetime
from typing import List, Optional

from pydantic import BaseModel, EmailStr, Extra, PositiveFloat, constr, validator


PHONE_REGEX_PATTERN = r"^\(\d{3}\) \d{3}-\d{4}$"  # (XXX) XXX-XXXX

PhoneNumberStr = constr(regex=PHONE_REGEX_PATTERN)


class CustomerCreate(BaseModel):
    name: str
    email: Optional[EmailStr]
    phone: Optional[PhoneNumberStr]
    notes: Optional[str]

    @validator("name")
    def normalize_name(cls, v):
        """Normalize for searching by name"""
        return v.lower()

    class Config:
        extra = Extra.forbid


class CustomerEdit(CustomerCreate):
    pass


class Customer(CustomerEdit):
    id: int
    date_created: datetime
    date_modified: datetime

    class Config:
        extra = Extra.forbid
        orm_mode = True


class MenuCategoryCreate(BaseModel):
    name: str

    class Config:
        extra = Extra.forbid


class MenuCategoryEdit(MenuCategoryCreate):
    pass


class MenuCategory(MenuCategoryEdit):
    id: int
    date_created: datetime
    date_modified: datetime

    class Config:
        extra = Extra.forbid
        orm_mode = True


class PriceUnits(str, enum.Enum):
    EACH = "each"
    DOZEN = "dozen"


class MenuItemCreate(BaseModel):
    name: str
    category_id: int
    description: Optional[str]
    price: PositiveFloat
    price_units: PriceUnits

    class Config:
        extra = Extra.forbid


class MenuItemEdit(MenuItemCreate):
    pass


class MenuItem(MenuItemEdit):
    id: int
    date_created: datetime
    date_modified: datetime
    category: MenuCategory

    class Config:
        extra = Extra.forbid
        orm_mode = True


class OrderItemCreateNewOrder(BaseModel):
    menu_item_id: int
    quantity: int
    menu_price: PositiveFloat
    charged_price: PositiveFloat
    notes: Optional[str]

    class Config:
        extra = Extra.forbid


class OrderItemCreate(OrderItemCreateNewOrder):
    order_id: int


class OrderItemEdit(OrderItemCreate):
    pass


class OrderItem(OrderItemEdit):
    id: int
    date_created: datetime
    date_modified: datetime
    menu_item: MenuItem

    class Config:
        extra = Extra.forbid
        orm_mode = True


class CampaignCreate(BaseModel):
    name: str
    description: str
    date_start: Optional[date]
    date_end: Optional[date]

    class Config:
        extra = Extra.forbid


class CampaignEdit(CampaignCreate):
    pass


class Campaign(CampaignEdit):
    id: int
    date_created: datetime
    date_modified: datetime

    class Config:
        extra = Extra.forbid
        orm_mode = True


class PaymentMethods(str, enum.Enum):
    CASH = "cash"
    ZELLE = "zelle"
    PAYPAL = "paypal"


class PaymentCreateNewOrder(BaseModel):
    amount: PositiveFloat
    method: PaymentMethods
    date: date

    class Config:
        extra = Extra.forbid


class PaymentCreate(PaymentCreateNewOrder):
    order_id: int


class PaymentEdit(PaymentCreate):
    pass


class Payment(PaymentEdit):
    id: int
    date_created: datetime
    date_modified: datetime

    class Config:
        extra = Extra.forbid
        orm_mode = True


class OrderEdit(BaseModel):
    customer_id: int
    campaign_id: Optional[int]
    date_ordered: Optional[date]
    date_delivered: Optional[date]
    price_adjustment: float = 0.0
    notes: Optional[str]
    completed: bool = False

    class Config:
        extra = Extra.forbid


class OrderCreate(OrderEdit):
    order_items: List[OrderItemCreateNewOrder]
    payments: List[PaymentCreateNewOrder] = []


class Order(OrderEdit):
    id: int
    date_created: datetime
    date_modified: datetime
    price_adjustment: float
    notes: Optional[str]
    completed: bool
    customer: Customer
    campaign: Optional[Campaign]
    order_items: List[OrderItem]
    payments: List[Payment]

    class Config:
        extra = Extra.forbid
        orm_mode = True
