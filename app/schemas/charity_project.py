from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field, PositiveInt

from app.core.config import MAX_LENGTH_NAME


class CharityProjectBase(BaseModel):
    name: Optional[str] = Field(None, min_length=1,
                                max_length=MAX_LENGTH_NAME)
    description: Optional[str] = Field(None,
                                       min_length=1)
    full_amount: Optional[PositiveInt]


class CharityProjectCreate(CharityProjectBase):
    name: str = Field(..., min_length=1,
                      max_length=MAX_LENGTH_NAME)
    description: str = Field(...,
                             min_length=1)
    full_amount: PositiveInt


class CharityProjectUpdate(CharityProjectBase):

    class Config:
        extra = Extra.forbid


class CharityProjectDB(CharityProjectBase):
    id: int
    invested_amount: Optional[int]
    create_date: Optional[datetime]
    close_date: Optional[datetime]
    fully_invested: Optional[bool]

    class Config:
        orm_mode = True
