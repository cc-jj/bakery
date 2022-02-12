from fastapi import APIRouter, Depends

from src.dependencies import get_authorized_user
from src.routes.v1 import campaigns, customers, menu, orders, payments, users

router = APIRouter(
    prefix="/v1",
    dependencies=[Depends(get_authorized_user)],
)

router.include_router(campaigns.router)
router.include_router(customers.router)
router.include_router(menu.router)
router.include_router(orders.router)
router.include_router(payments.router)
router.include_router(users.router)
