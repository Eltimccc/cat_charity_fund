# app/models/charityproject.py
from sqlalchemy import Column, ForeignKey, String, Text, Integer, Boolean, DateTime
from datetime import datetime
from sqlalchemy.orm import relationship

from app.core.db import Base


# class CharityProject(Base):
#     name = Column(String(100), unique=True, nullable=False)
#     description = Column(Text)
#     full_amount = Column(Integer)
#     id = Column(Integer, primary_key=True, index=True)
#     invested_amount = Column(Integer, default=0)
#     fully_invested = Column(Boolean, default=False)
#     create_date = Column(DateTime, default=datetime.now())
#     close_date = Column(DateTime, default=datetime.now())

#     donations = relationship("Donation", back_populates="project", primaryjoin="CharityProject.id == Donation.project_id")



class CharityProject(Base):

    name = Column(String(100),unique=True, nullable=False)
    description = Column(Text)
    full_amount = Column(Integer)
    id = Column(Integer, primary_key=True, index=True)
    invested_amount = Column(Integer, default=0)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime,
                         default=datetime.now())
    close_date = Column(DateTime,
                        default=datetime.now())

    def can_delete(self):
        return self.invested_amount == 0