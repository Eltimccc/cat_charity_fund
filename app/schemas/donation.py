from datetime import datetime
from typing import Optional

from pydantic import BaseModel, PositiveInt


class DonationBase(BaseModel):
    comment: Optional[str] = None
    create_date: Optional[datetime]
    full_amount: PositiveInt
    id: int
    user_id: Optional[int] = None
    invested_amount: Optional[int] = 0
    fully_invested: bool = False


class DonationCreate(BaseModel):
    comment: Optional[str] = None
    full_amount: PositiveInt
    user_id: Optional[int] = None
    invested_amount: Optional[int] = 0
    fully_invested: bool = False


class DonationDB(DonationBase):
    id: int
    user_id: Optional[int] = None

    class Config:
        orm_mode = True


class DonationMyDB(BaseModel):
    full_amount: PositiveInt
    comment: str
    id: int
    create_date: Optional[datetime]
