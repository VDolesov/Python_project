from fastapi import APIRouter, HTTPException, status
from project.infrastructure.postgres.repository.bookings_repo import BookingsRepository
from project.infrastructure.postgres.database import PostgresDatabase
from project.schemas.bookings import BookingSchema, BookingCreateUpdateSchema
from project.core.exceptions import (
    ClientNotFound,
    RoomTypeNotFound,
    HotelNotFound,
    BookingNotFound,
    BookingAlreadyExists,
)

router = APIRouter()
bookings_repo = BookingsRepository()
database = PostgresDatabase()

@router.get(
    "/all_bookings",
    response_model=list[BookingSchema],
    status_code=status.HTTP_200_OK,
)
async def get_all_bookings() -> list[BookingSchema]:
    async with database.session() as session:
        await bookings_repo.check_connection(session=session)
        all_bookings = await bookings_repo.get_all_bookings(session=session)
    return all_bookings


@router.get(
    "/booking/{booking_id}",
    response_model=BookingSchema,
    status_code=status.HTTP_200_OK,
)
async def get_booking_by_id(booking_id: int) -> BookingSchema:
    async with database.session() as session:
        try:
            booking = await bookings_repo.get_booking_by_id(session=session, booking_id=booking_id)
        except BookingNotFound as error:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
    return booking


@router.post(
    "/add_booking",
    response_model=BookingSchema,
    status_code=status.HTTP_201_CREATED,
)
async def add_booking(booking_dto: BookingCreateUpdateSchema) -> BookingSchema:
    async with database.session() as session:
        try:
            new_booking = await bookings_repo.create_booking(session=session, booking=booking_dto)
        except ClientNotFound as error:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Client not found"
            )
        except RoomTypeNotFound as error:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Room type not found"
            )
        except HotelNotFound as error:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Hotel not found"
            )
        except BookingAlreadyExists as error:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Booking already exists"
            )
    return new_booking


@router.put(
    "/update_booking/{booking_id}",
    response_model=BookingSchema,
    status_code=status.HTTP_200_OK,
)
async def update_booking(
    booking_id: int, booking_dto: BookingCreateUpdateSchema
) -> BookingSchema:
    async with database.session() as session:
        try:
            updated_booking = await bookings_repo.update_booking(
                session=session, booking_id=booking_id, booking=booking_dto
            )
        except BookingNotFound as error:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
    return updated_booking


@router.delete(
    "/delete_booking/{booking_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_booking(booking_id: int) -> None:
    async with database.session() as session:
        try:
            await bookings_repo.delete_booking(session=session, booking_id=booking_id)
        except BookingNotFound as error:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
