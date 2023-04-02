# app/schemas/charityproject.py
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, validator


class DonationBase(BaseModel):
    full_amount: int
    comment: Optional[str] = None
    invested_amount: Optional[int] = 0
    fully_invested: bool = False
    create_date: Optional[datetime] = None
    close_date: Optional[datetime] = None


class DonationCreate(DonationBase):
    pass


class DonationUpdate(DonationBase):
    pass


class DonationDB(DonationBase):
    id: int
    user_id: Optional[int] = None

    class Config:
        orm_mode = True

