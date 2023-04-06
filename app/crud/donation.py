# # app/crud/reservation.py
from typing import Optional

from sqlalchemy import and_, select
# from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.crud.base import CRUDBase
from app.models import Donation, User
from app.models.donation import Donation
from app.schemas.donation import DonationMyDB


class CRUDDonation(CRUDBase):

    async def get_all_donation(
            self,
            user_id: int,
            session: AsyncSession,
    ) -> Optional[int]:
        db_donation_id = await session.execute(
            select(Donation.id)
            .where(
                and_(Donation.user_id == user_id,
                     Donation.response.isnot(None))
            )
        )
        db_donation_id = db_donation_id.scalars().first()

        return db_donation_id


    async def get_by_user(
            self, session: AsyncSession, user: User
            ):
        donations = await session.execute(
            select(Donation
                   ).where(
            Donation.user_id == user.id)
            )
        donations_list = [
            donation.__dict__
            for donation in donations.scalars().all()
            ]
        donations_db = [DonationMyDB(**donation_dict)
                        for donation_dict in donations_list]
        return donations_db

donation_crud = CRUDDonation(Donation)
        

