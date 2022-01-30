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
    id: int


class Customer(CustomerEdit):
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
    id: int


class MenuCategory(MenuCategoryEdit):
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
    id: int


class MenuItem(MenuItemEdit):
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
    id: int


class OrderItem(OrderItemEdit):
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
    id: int


class Campaign(CampaignEdit):
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
    id: int


class Payment(PaymentEdit):
    date_created: datetime
    date_modified: datetime

    class Config:
        extra = Extra.forbid
        orm_mode = True


class _OrderCommon(BaseModel):
    customer_id: int
    campaign_id: Optional[int]
    date_ordered: Optional[date]
    date_delivered: Optional[date]
    price_adjustment: float = 0.0
    notes: Optional[str]
    completed: bool = False

    class Config:
        extra = Extra.forbid


class OrderCreate(_OrderCommon):
    order_items: List[OrderItemCreateNewOrder]
    payments: List[PaymentCreateNewOrder] = []


class OrderEdit(_OrderCommon):
    id: int


class Order(_OrderCommon):
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
