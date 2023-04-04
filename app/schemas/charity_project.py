# app/schemas/charityproject.py
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, validator


class CharityProjectBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1)
    full_amount: Optional[int] = 0
    id: Optional[int] = Field(None, title="id")
    invested_amount: int = Field(default=0, ge=0)
    fully_invested: bool = Field(default=False)
    create_date: Optional[datetime]
    close_date: Optional[datetime]


class CharityProjectCreateRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1)
    full_amount: Optional[int] = 0


class CharityProjectCreateResponse(CharityProjectBase):
    id: int
    invested_amount: int = Field(default=0, ge=0)
    fully_invested: bool = Field(default=False)

    class Config:
        orm_mode = True
        allow_population_by_field_name = True

class CharityProjectCreate(CharityProjectBase):
    name: str = Field(..., min_length=1, max_length=100)


class CharityProjectUpdate(CharityProjectBase):
    
    @validator('name')
    def name_cannot_be_null(cls, value):
        if value is None:
            raise ValueError('Имя не может быть пустым!')
        return value


class CharityProjectDB(CharityProjectCreate):
    id: int

    class Config:
        orm_mode = True
        allow_population_by_field_name = True

