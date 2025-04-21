from fastapi import APIRouter, HTTPException, status

from project.infrastructure.postgres.repository.hotels_repo import HotelsRepository
from project.infrastructure.postgres.database import PostgresDatabase
from project.schemas.hotels import HotelSchema, HotelCreateUpdateSchema
from project.core.exceptions import HotelNotFound, HotelAlreadyExists

router = APIRouter()
hotels_repo = HotelsRepository()
database = PostgresDatabase()

@router.get(
    "/all_hotels",
    response_model=list[HotelSchema],
    status_code=status.HTTP_200_OK
)
async def get_all_hotels() -> list[HotelSchema]:
    async with database.session() as session:
        await hotels_repo.check_connection(session=session)
        all_hotels = await hotels_repo.get_all_hotels(session=session)
    return all_hotels


@router.get(
    "/hotel/{hotel_id}",
    response_model=HotelSchema,
    status_code=status.HTTP_200_OK
)
async def get_hotel_by_id(hotel_id: int) -> HotelSchema:
    async with database.session() as session:
        try:
            hotel = await hotels_repo.get_hotel(session=session, hotel_id=hotel_id)
        except HotelNotFound as error:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
    return hotel


@router.post(
    "/add_hotel",
    response_model=HotelSchema,
    status_code=status.HTTP_201_CREATED
)
async def add_hotel(hotel_dto: HotelCreateUpdateSchema) -> HotelSchema:
    async with database.session() as session:
        try:
            new_hotel = await hotels_repo.create_hotel(session=session, hotel=hotel_dto)
        except HotelAlreadyExists as error:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=error.message)
    return new_hotel


@router.put(
    "/update_hotel/{hotel_id}",
    response_model=HotelSchema,
    status_code=status.HTTP_200_OK
)
async def update_hotel(hotel_id: int, hotel_dto: HotelCreateUpdateSchema) -> HotelSchema:
    async with database.session() as session:
        try:
            updated_hotel = await hotels_repo.update_hotel(session=session, hotel_id=hotel_id, hotel=hotel_dto)
        except HotelNotFound as error:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
    return updated_hotel


@router.delete(
    "/delete_hotel/{hotel_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_hotel(hotel_id: int) -> None:
    async with database.session() as session:
        try:
            await hotels_repo.delete_hotel(session=session, hotel_id=hotel_id)
        except HotelNotFound as error:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
