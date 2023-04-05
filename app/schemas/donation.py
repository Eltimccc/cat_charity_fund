# app/schemas/charityproject.py
from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class DonationBase(BaseModel):
    comment: Optional[str] = None
    create_date: Optional[datetime]
    full_amount: int
    id: int
    user_id: Optional[int] = None
    invested_amount: Optional[int] = 0
    fully_invested: bool = False


class DonationCreate(BaseModel):
    comment: Optional[str] = None
    full_amount: int
    user_id: Optional[int] = None
    invested_amount: Optional[int] = 0
    fully_invested: bool = False


class DonationDB(DonationBase):
    id: int
    user_id: Optional[int] = None

    class Config:
        orm_mode = True

class DonationMyDB(BaseModel):
    full_amount: int
    comment: str
    id: int
    create_date: Optional[datetime]
