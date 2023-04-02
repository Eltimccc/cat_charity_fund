# app/models/donation.py
# Импортируйте классы.
from sqlalchemy import DateTime, ForeignKey,Column, String, Text, Integer, Boolean, DateTime

from datetime import datetime
from app.core.db import Base


class Donation(Base):
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(
      Integer, 
      ForeignKey('user.id', name='fk_donation_user_id_user')
  )
    comment = Column(Text)
    full_amount  = Column(Integer)
    invested_amount = Column(Integer, default=0)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime,
                         default=datetime.now())
    close_date = Column(DateTime,
                        default=datetime.now())


    # def __repr__(self):
    #     return (
    #         f'Уже забронировано с {self.from_reserve} по {self.to_reserve}'
    #     )

