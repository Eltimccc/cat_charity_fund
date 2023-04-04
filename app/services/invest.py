from sqlalchemy import and_, select
from sqlalchemy.orm import Session
from typing import List
from app.core.db import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Donation, CharityProject
from app.schemas.charity_project import CharityProjectCreateRequest


'''ДОДЕЛАТЬ!!'''
async def create_project(charity_project: CharityProjectCreateRequest, session: AsyncSession) -> List[Donation]:
    await session.flush()

    result_proxy = await session.execute(select(Donation).where(
    and_(
        Donation.fully_invested == False,
        Donation.invested_amount == 0
    )
))
    unallocated_donations = [row for row in result_proxy.scalars()]

    full_amount = charity_project.full_amount
    total_amount = 0
    for donation in unallocated_donations:
        if total_amount >= full_amount:
            break
        donation.invested_amount = donation.full_amount
        donation.fully_invested = True
        total_amount += donation.full_amount

    await session.commit()

    return unallocated_donations