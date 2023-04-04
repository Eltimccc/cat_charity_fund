from sqlalchemy import and_, select
from sqlalchemy.orm import Session
from typing import List, Tuple
from app.core.db import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Donation, CharityProject
from app.schemas.charity_project import CharityProjectCreateRequest
from app.crud.charity_project import charity_project_crud


'''ДОДЕЛАТЬ!!'''


async def create_project(
    charity_project: CharityProjectCreateRequest,
    session: AsyncSession
) -> Tuple[CharityProject, List[Donation]]:
    async with session.begin():
        unallocated_donations = await session.execute(select(Donation).where(
            and_(
                Donation.fully_invested == False,
                Donation.invested_amount == 0
            )
        )).scalars().all()

        full_amount = charity_project.full_amount
        total_amount = 0
        for donation in unallocated_donations:
            if total_amount >= full_amount:
                break
            donation.invested_amount = donation.full_amount
            donation.fully_invested = True
            total_amount += donation.full_amount

        new_project = await charity_project_crud.create(charity_project, session)
        await session.commit()

        return new_project, unallocated_donations
