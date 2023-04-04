from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.api.validators import check_name_duplicate
from app.core.db import get_async_session
from app.crud.donation import CRUDDonation, donation_crud
from app.crud.charity_project import charity_project_crud
from app.core.user import current_superuser
from app.schemas.charity_project import CharityProjectCreateRequest, CharityProjectCreateResponse
from app.schemas.donation import DonationDB, DonationCreate, DonationMyDB
from app.models.donation import Donation
from app.core.user import current_user
from app.models import User

from sqlalchemy.orm import Session, selectinload
from app.models import Donation, CharityProject
# from app.services.invest import invest
from sqlalchemy.future import select

from app.services.invest import create_project
# from app.api.dependencies import get_db, get_current_user

router = APIRouter()

### вот эту переделать тоже
@router.post(
    '/',
    response_model=CharityProjectCreateResponse,
    dependencies=[Depends(current_superuser)]
)
async def create_new_charity_project(
        charity_project: CharityProjectCreateRequest,
        session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""
    await check_name_duplicate(charity_project.name, session)
    

    await create_project(charity_project, session)
    new_project = await charity_project_crud.create(charity_project, session)

    return CharityProjectCreateResponse(**new_project.__dict__)


# @router.post(
#     '/',
#     response_model=DonationDB,
#     response_model_exclude_none=True,
# )
# async def create_new_donation(
#         charity_project: DonationCreate,
#         session: AsyncSession = Depends(get_async_session),
#         user: User = Depends(current_user)
# ):
#     """Для пользователей."""

#     new_donation = await donation_crud.create(
#         charity_project, session, user
#     )
#     return new_donation


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
