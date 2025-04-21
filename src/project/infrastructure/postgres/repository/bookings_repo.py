from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from project.infrastructure.postgres.models import Booking, Client, RoomType, Hotel
from project.schemas.bookings import BookingCreateUpdateSchema, BookingSchema
from project.core.exceptions import (
    ClientNotFound,
    RoomTypeNotFound,
    HotelNotFound,
    BookingNotFound,
    BookingAlreadyExists,
)


class BookingsRepository:
    async def check_connection(self, session: AsyncSession) -> bool:
        try:
            await session.execute(select(1))
            return True
        except Exception:
            return False

    async def get_all_bookings(self, session: AsyncSession) -> list[BookingSchema]:
        result = await session.execute(select(Booking))
        return [BookingSchema.model_validate(obj=booking) for booking in result.scalars().all()]

    async def get_booking_by_id(self, session: AsyncSession, booking_id: int) -> Booking:
        result = await session.execute(select(Booking).where(Booking.booking_id == booking_id))
        booking = result.scalars().first()
        if not booking:
            raise BookingNotFound()
        return booking

    async def create_booking(self, session: AsyncSession, booking: BookingCreateUpdateSchema) -> Booking:
        # Проверяем, существует ли клиент
        client_result = await session.execute(select(Client).where(Client.client_id == booking.client_id))
        if not client_result.scalars().first():
            raise ClientNotFound()

        # Проверяем, существует ли тип комнаты
        room_type_result = await session.execute(
            select(RoomType).where(RoomType.room_type_id == booking.room_type_id)
        )
        if not room_type_result.scalars().first():
            raise RoomTypeNotFound()

        # Проверяем, существует ли отель
        hotel_result = await session.execute(select(Hotel).where(Hotel.hotel_id == booking.hotel_id))
        if not hotel_result.scalars().first():
            raise HotelNotFound()

        # Создаем новое бронирование
        new_booking = Booking(
            client_id=booking.client_id,
            room_type_id=booking.room_type_id,
            hotel_id=booking.hotel_id,
            booking_date=booking.booking_date,
            check_in_date=booking.check_in_date,
            check_out_date=booking.check_out_date,
        )
        session.add(new_booking)
        await session.commit()
        await session.refresh(new_booking)
        return new_booking

    async def update_booking(
        self, session: AsyncSession, booking_id: int, booking: BookingCreateUpdateSchema
    ) -> Booking:
        result = await session.execute(select(Booking).where(Booking.booking_id == booking_id))
        existing_booking = result.scalars().first()
        if not existing_booking:
            raise BookingNotFound()

        existing_booking.client_id = booking.client_id
        existing_booking.room_type_id = booking.room_type_id
        existing_booking.hotel_id = booking.hotel_id
        existing_booking.booking_date = booking.booking_date
        existing_booking.check_in_date = booking.check_in_date
        existing_booking.check_out_date = booking.check_out_date

        await session.commit()
        await session.refresh(existing_booking)
        return existing_booking

    async def delete_booking(self, session: AsyncSession, booking_id: int) -> None:
        result = await session.execute(select(Booking).where(Booking.booking_id == booking_id))
        booking = result.scalars().first()
        if not booking:
            raise BookingNotFound()

        await session.delete(booking)
        await session.commit()
