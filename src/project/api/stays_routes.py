from fastapi import APIRouter, HTTPException, status
from datetime import date
from project.infrastructure.postgres.repository.stays_repo import StaysRepository
from project.infrastructure.postgres.database import PostgresDatabase
from project.schemas.stays import StaySchema, StayCreateUpdateSchema
from project.core.exceptions import (
    StayNotFound,
    RoomNotFound,
    BookingNotFound,
    StayAlreadyExists,
    InvalidStayDates,
    InvalidPaymentAmount,
)
router = APIRouter()
stays_repo = StaysRepository()
database = PostgresDatabase()

@router.get(
    "/all_stays",
    response_model=list[StaySchema],
    status_code=status.HTTP_200_OK
)
async def get_all_stays() -> list[StaySchema]:
    async with database.session() as session:
        await stays_repo.check_connection(session=session)
        all_stays = await stays_repo.get_all_stays(session=session)
    return all_stays


@router.get(
    "/stay/{stay_id}",
    response_model=StaySchema,
    status_code=status.HTTP_200_OK
)
async def get_stay_by_id(stay_id: int) -> StaySchema:
    async with database.session() as session:
        try:
            stay = await stays_repo.get_stay(session=session, stay_id=stay_id)
        except StayNotFound as error:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
    return stay


@router.post(
    "/add_stay",
    response_model=StaySchema,
    status_code=status.HTTP_201_CREATED
)
async def add_stay(stay_dto: StayCreateUpdateSchema) -> StaySchema:
    # Валидация дат check_in_date и check_out_date
    if stay_dto.check_in_date >= stay_dto.check_out_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=InvalidStayDates().message
        )

    # Валидация поля payment
    if stay_dto.payment < 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=InvalidPaymentAmount(message="Payment must be greater than or equal to 0").message
        )

    async with database.session() as session:
        try:
            new_stay = await stays_repo.create_stay(session=session, stay=stay_dto)
        except RoomNotFound as error:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
        except BookingNotFound as error:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
        except StayAlreadyExists as error:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=error.message)
    return new_stay

@router.put(
    "/update_stay/{stay_id}",
    response_model=StaySchema,
    status_code=status.HTTP_200_OK
)
async def update_stay(stay_id: int, stay_dto: StayCreateUpdateSchema) -> StaySchema:
    async with database.session() as session:
        try:
            updated_stay = await stays_repo.update_stay(
                session=session, stay_id=stay_id, stay=stay_dto
            )
        except StayNotFound as error:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
    return updated_stay


@router.delete(
    "/delete_stay/{stay_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_stay(stay_id: int) -> None:
    async with database.session() as session:
        try:
            await stays_repo.delete_stay(session=session, stay_id=stay_id)
        except StayNotFound as error:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
