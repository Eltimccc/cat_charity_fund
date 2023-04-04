# app/schemas/charityproject.py
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, validator, PositiveInt


class CharityProjectBase(BaseModel):
    create_date: Optional[datetime]
    description: str = Field(..., min_length=1)
    full_amount: PositiveInt
    fully_invested: bool = Field(default=False)
    id: Optional[int] = Field(None, title="id")
    invested_amount: int = Field(default=0, ge=0)
    name: str = Field(..., min_length=1, max_length=100)
    

class CharityProjectCreateRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1)
    full_amount: PositiveInt


class CharityProjectDeleteResponse(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1)
    full_amount: PositiveInt
    id: Optional[int] = Field(None, title="id")
    invested_amount: int = Field(default=0, ge=0)
    fully_invested: bool = Field(default=False)
    create_date: Optional[datetime]
    close_date: Optional[datetime]


class CharityProjectCreateResponse(CharityProjectBase):
    description: str = Field(..., min_length=1)
    full_amount: PositiveInt
    fully_invested: bool = Field(default=False)
    id: Optional[int] = Field(None, title="id")
    invested_amount: int = Field(default=0, ge=0)
    name: str = Field(..., min_length=1, max_length=100)


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

    @validator('full_amount', always=True)
    def check_full_amount(cls, value, values):
        if 'invested_amount' in values and value < values['invested_amount']:
            raise ValueError('Требуемая сумма не может быть меньше внесенной!')
        else:
            return value

class CharityProjectDB(CharityProjectCreate):
    id: int

    class Config:
        orm_mode = True
        allow_population_by_field_name = True

