from datetime import datetime
from typing import Type

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Donation
from app.schemas.charity_project import CharityProjectCreate


async def allocate_donations(
    project: CharityProjectCreate,
    donation_model: Type[Donation],
    session: AsyncSession
) -> CharityProjectCreate:
    """Распределение донатов."""

    unallocated_donations = await session.execute(
        select(donation_model).where(
            donation_model.fully_invested == False
        ).order_by(donation_model.create_date)
    )
    unallocated_donations = unallocated_donations.scalars().all()

    amount_left = sum(donation.full_amount - donation.invested_amount for donation in unallocated_donations)
    for donation in unallocated_donations:
        amount_to_invest = min(
            project.full_amount -
            project.invested_amount,
            donation.full_amount -
            donation.invested_amount,
            amount_left
        )
        project.invested_amount += amount_to_invest
        donation.invested_amount += amount_to_invest
        amount_left -= amount_to_invest
        if project.invested_amount >= project.full_amount:
            project.fully_invested = True
            project.close_date = datetime.now()
        if donation.invested_amount >= donation.full_amount:
            donation.fully_invested = True
            donation.close_date = datetime.now()
        
        session.add(project)
        session.add(donation)
        
        if amount_left == 0:
            break

    await session.commit()
    await session.refresh(project)

    return project
