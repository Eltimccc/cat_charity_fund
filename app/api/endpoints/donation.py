from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.crud.donation import donation_crud
from app.core.user import current_superuser
from app.schemas.donation import DonationDB, DonationCreate
from app.models.donation import Donation

router = APIRouter()

### Исправить POST
@router.post(
    '/',
    response_model=DonationDB,
    response_model_exclude_unset=True,
)
async def create_donation(
        donation: DonationCreate,
        session: AsyncSession = Depends(get_async_session),
):
    db_donation = Donation(**donation.dict())
    session.add(db_donation)
    await session.commit()
    await session.refresh(db_donation)
    return db_donation


@router.get(
    '/',
    response_model=list[DonationDB],
    response_model_exclude_none=True,
)
async def get_all_donation(
        session: AsyncSession = Depends(get_async_session),
):
    all_donation = await donation_crud.get_multi(session)
    return all_donation
