from http import HTTPStatus
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models import CharityProject, charity_project
from app.schemas.charity_project import CharityProjectDB


async def check_name_duplicate(
        charity_project: str,
        session: AsyncSession,
) -> None:
    charity_project_id = await charity_project_crud.get_charity_project(charity_project, session)
    if charity_project_id is not None:
        raise HTTPException(
            status_code=400,
            detail='Проект с таким именем уже существует!',
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


async def validate_project_not_fully_invested(
    project: CharityProjectDB,
    session: AsyncSession,
):
    if project.fully_invested:
        raise HTTPException(
            status_code=423,
            detail='Закрытый проект нельзя редактировать!'
        )
    return project


def validate_project_updated_amount(new_amount: int, current_amount: int, session) -> None:
    # print('new', new_amount)
    # print('current', current_amount)
    if new_amount < current_amount:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail='Нельзя установить требуемую сумму меньше вложенной'
        )
    else:
        return HTTPStatus.OK


async def check_charity_project_has_investment(
    charity_project: CharityProject,
    session: AsyncSession,
) -> None:
    if charity_project.invested_amount:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='В проект были внесены средства, не подлежит удалению!'
        )


    # if project.fully_invested:
    #     raise HTTPException(status_code = 400, detail = "Закрытый проект нельзя редактировать!")
    # return True


# def check_fully_invested(charity_project: CharityProjectDB):
#     if charity_project.fully_invested:
#         raise HTTPException(status_code=400, detail="Проект полностью проинвестирован")
#     return True