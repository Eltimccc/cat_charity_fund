from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.core.db import get_async_session
from app.crud.donation import donation_crud
from app.core.user import current_superuser
from app.schemas.donation import DonationDB, DonationCreate, DonationMyDB
from app.core.user import current_user
from app.models import User
from app.models import CharityProject


router = APIRouter()


@router.post(
    '/',
    response_model=DonationDB,
    response_model_exclude_none=True,
)
async def create_new_donation(
        donation: DonationCreate,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user)
):
    """Для пользователей."""

    new_donation = await donation_crud.create(donation, session, user)

    projects = await session.execute(select(CharityProject))
    projects = projects.scalars().all()

    amount_left = new_donation.full_amount
    for project in projects:
        if project.fully_invested:
            continue
        amount_to_invest = min(project.full_amount - project.invested_amount, amount_left)
        project.invested_amount += amount_to_invest
        amount_left -= amount_to_invest
        if project.invested_amount >= project.full_amount:
            project.fully_invested = True
            project.close_date = datetime.now()
        session.add(project)
        if amount_left == 0:
            break

    new_donation.invested_amount = new_donation.full_amount - amount_left
    new_donation.fully_invested = (amount_left == 0)
    new_donation.close_date = datetime.now()
    session.add(new_donation)
    await session.commit()

    return new_donation


@router.get(
    '/',
    response_model=List[DonationDB],
    dependencies=[Depends(current_superuser)],
    response_model_exclude_none=True,
)
async def get_all_donation(
        session: AsyncSession = Depends(get_async_session),
):
    ''' Только для суперюзеров. '''
    all_donation = await donation_crud.get_multi(session)
    return all_donation


@router.get(
    '/my', response_model=List[DonationMyDB],
    response_model_exclude={'user_id'},
)
async def get_my_donation(
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user)
):
    """Получает список всех донатов текущего пользователя."""
    reservations = await donation_crud.get_by_user(
        session=session, user=user
    )
    return reservations
