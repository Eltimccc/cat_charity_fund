from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.donation import donation_crud
from app.models import CharityProject, User
from app.schemas.donation import DonationCreate, DonationDB, DonationMyDB
from app.services.invest import add_new_donation_to_db

router = APIRouter()


@router.post(
    '/',
    response_model=DonationDB,
    response_model_exclude_none=True,
    response_model_exclude=('user_id',
                            'fully_invested',
                            'invested_amount'),
)
async def create_new_donation(
        donation: DonationCreate,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user)
):
    new_donation = await donation_crud.create(donation, session, user)

    projects = await session.execute(select(CharityProject))
    projects = projects.scalars().all()

    await add_new_donation_to_db(new_donation, projects, session)

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
    reservations = await donation_crud.get_by_user(
        session=session, user=user
    )
    return reservations
