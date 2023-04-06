from datetime import datetime
from typing import List, Type

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Donation
from app.models.charity_project import CharityProject
from app.schemas.charity_project import CharityProjectCreate
from app.schemas.donation import DonationDB


async def add_new_donation_to_db(donation: DonationDB,
                                 projects: List[CharityProject],
                                 session: AsyncSession):
    amount_left = donation.full_amount
    for project in projects:
        if project.fully_invested:
            continue
        amount_to_invest = min(project.full_amount -
                               project.invested_amount,
                               amount_left)
        project.invested_amount += amount_to_invest
        amount_left -= amount_to_invest
        if project.invested_amount >= project.full_amount:
            project.fully_invested = True
            project.close_date = datetime.now()
        session.add(project)
        if amount_left == 0:
            break

    donation.invested_amount = donation.full_amount - amount_left
    donation.fully_invested = (amount_left == 0)
    donation.close_date = datetime.now()
    session.add(donation)

    await session.commit()
    await session.refresh(donation)


async def allocate_donations(
    project: CharityProjectCreate,
    donation_model: Type[Donation],
    session: AsyncSession
) -> CharityProjectCreate:
    """
    Распределение донатов после создания проекта.
    """

    unallocated_donations = (
        await session.execute(
            select(donation_model)
            .where(donation_model.fully_invested.is_(False))
            .order_by(donation_model.create_date)
        )
    ).scalars().all()

    amount_left = sum(
        donation.full_amount - donation.invested_amount
        for donation in unallocated_donations
    )

    for donation in unallocated_donations:
        amount_to_invest = min(
            project.full_amount - project.invested_amount,
            donation.full_amount - donation.invested_amount,
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
