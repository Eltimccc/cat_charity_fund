from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models import CharityProject


async def check_name_duplicate(
        charity_project: str,
        session: AsyncSession,
) -> None:
    charity_project_id = await charity_project_crud.get_charity_project(charity_project, session)
    if charity_project_id is not None:
        raise HTTPException(
            status_code=422,
            detail='Такое имя уже существует!',
        )
    

async def check_charity_project_exists(
        charity_project_id: int,
        session: AsyncSession,
) -> CharityProject:
    charity_project = await charity_project_crud.get(charity_project_id, session)
    if charity_project is None:
        raise HTTPException(
            status_code=404,
            detail='ID не найдено!'
        )
    return charity_project