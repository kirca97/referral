from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, typing


class PlanBase(BaseModel):
    name: str
    num_servers: int
    price: int

class Plan(PlanBase):
    id: int

    class Config:
        orm_mode = True

class UserBase(BaseModel):
    referral_link: str
    credits: float
    administrator: bool
    referraled_id: Optional[int]

class User(UserBase):
    id: int

    class Config:
        orm_mode = True

class VoucherBase(BaseModel):
    amount: float
    start_date: datetime


# class VoucherCreate(VoucherBase):


class Voucher(VoucherBase):
    id: int
    code: str
    is_used: bool
    end_date: Optional[datetime]
    user_id: Optional[int]

    class Config:
        orm_mode = True

class PromoCodeBase(BaseModel):
    discount_percentage: float
    start_date: datetime


class PromoCode(PromoCodeBase):
    code: str
    is_used: bool
    end_date: Optional[datetime]
    user_id: Optional[int]
    id: int

    class Config:
        orm_mode = True

class SuccessfulPayment(BaseModel):
    user_id: int
    amount: float
    credits: float
    promo_code: Optional[str]

    class Config:
        orm_mode = True