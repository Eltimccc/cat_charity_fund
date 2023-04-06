from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text
from app.core.config import MAX_LENGTH_NAME

from app.core.db import Base


class CharityProject(Base):

    name = Column(String(MAX_LENGTH_NAME), unique=True, nullable=False)
    description = Column(Text)
    full_amount = Column(Integer)
    id = Column(Integer, primary_key=True, index=True)
    invested_amount = Column(Integer, default=0)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, default=datetime.now)
    close_date = Column(DateTime, default=None, nullable=True)

    def can_delete(self):
        return self.invested_amount == 0
