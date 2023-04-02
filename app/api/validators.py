from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
# from app.models import MeetingRoom, Reservation
# from app.crud.reservation import reservation_crud
# from app.models import MeetingRoom, Reservation, User


async def check_name_duplicate(
        room_name: str,
        session: AsyncSession,
) -> None:
    room_id = await charity_project_crud.get_room_id_by_name(room_name, session)
    if room_id is not None:
        raise HTTPException(
            status_code=422,
            detail='Переговорка с таким именем уже существует!',
        )