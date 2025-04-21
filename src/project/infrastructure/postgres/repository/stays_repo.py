from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from project.infrastructure.postgres.models import Stay,Room
from project.schemas.stays import StayCreateUpdateSchema, StaySchema
from project.core.exceptions import StayNotFound, RoomNotFoundInStays,RoomNotFound
from project.infrastructure.postgres.models import Stay, Room, Booking
from project.core.exceptions import BookingNotFound

class StaysRepository:
    async def check_connection(self, session: AsyncSession) -> bool:
        try:
            await session.execute(select(1))
            return True
        except Exception:
            return False

    async def get_all_stays(self, session: AsyncSession) -> list[StaySchema]:
        result = await session.execute(select(Stay))
        return [StaySchema.model_validate(obj=stay) for stay in result.scalars().all()]

    async def create_stay(self, session: AsyncSession, stay: StayCreateUpdateSchema) -> Stay:
        # Проверяем, существует ли room_id в таблице rooms
        room_check = await session.execute(
            select(Room).where(Room.room_id == stay.room_id)
        )
        if not room_check.scalars().first():
            raise RoomNotFound()

        # Проверяем, существует ли booking_id в таблице bookings
        booking_check = await session.execute(
            select(Booking).where(Booking.booking_id == stay.booking_id)
        )
        if not booking_check.scalars().first():
            raise BookingNotFound()

        # Создание нового Stay
        new_stay = Stay(
            room_id=stay.room_id,
            booking_id=stay.booking_id,
            payment=stay.payment,
            check_in_date=stay.check_in_date,
            check_out_date=stay.check_out_date,
            type_payment_id=stay.type_payment_id,
            total_price=stay.total_price,
        )
        session.add(new_stay)
        await session.commit()
        await session.refresh(new_stay)
        return new_stay

    async def update_stay(self, session: AsyncSession, stay_id: int, stay: StayCreateUpdateSchema) -> Stay:
        result = await session.execute(select(Stay).where(Stay.stay_id == stay_id))
        existing_stay = result.scalars().first()
        if not existing_stay:
            raise StayNotFound()

        existing_stay.room_id = stay.room_id
        existing_stay.booking_id = stay.booking_id
        existing_stay.payment = stay.payment
        existing_stay.check_in_date = stay.check_in_date
        existing_stay.check_out_date = stay.check_out_date
        existing_stay.type_payment_id = stay.type_payment_id
        existing_stay.date_payment_id = stay.date_payment_id
        existing_stay.total_price = stay.total_price
        await session.commit()
        await session.refresh(existing_stay)
        return existing_stay

    async def delete_stay(self, session: AsyncSession, stay_id: int) -> None:
        result = await session.execute(select(Stay).where(Stay.stay_id == stay_id))
        stay = result.scalars().first()
        if not stay:
            raise StayNotFound()

        await session.delete(stay)
        await session.commit()
