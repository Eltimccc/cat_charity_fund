# # app/crud/reservation.py
from app.crud.base import CRUDBase
from app.models.donation import Donation
from app.models import Donation, User
# from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import and_, select
from typing import Optional


class CRUDDonation(CRUDBase):

    async def get_donation_by_username(
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

donation_crud = CRUDDonation(Donation)
