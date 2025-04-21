from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from project.infrastructure.postgres.models import Hotel
from project.schemas.hotels import HotelCreateUpdateSchema, HotelSchema
from project.core.exceptions import HotelNotFound, HotelAlreadyExists


class HotelsRepository:
    async def check_connection(self, session: AsyncSession) -> bool:
        try:
            await session.execute(select(1))
            return True
        except Exception:
            return False

    async def get_all_hotels(self, session: AsyncSession) -> list[HotelSchema]:
        result = await session.execute(select(Hotel))
        return [HotelSchema.model_validate(obj=hotel) for hotel in result.scalars().all()]

    async def get_hotel(self, session: AsyncSession, hotel_id: int) -> Hotel:
        """Добавленный метод для получения отеля по ID"""
        result = await session.execute(select(Hotel).where(Hotel.hotel_id == hotel_id))
        hotel = result.scalars().first()
        if not hotel:
            raise HotelNotFound()
        return hotel

    async def create_hotel(self, session: AsyncSession, hotel: HotelCreateUpdateSchema) -> Hotel:
        existing_hotel = await session.execute(
            select(Hotel).where(Hotel.name == hotel.name, Hotel.address == hotel.address)
        )
        if existing_hotel.scalars().first():
            raise HotelAlreadyExists()

        new_hotel = Hotel(name=hotel.name, address=hotel.address)
        session.add(new_hotel)
        await session.commit()
        await session.refresh(new_hotel)
        return new_hotel

    async def update_hotel(self, session: AsyncSession, hotel_id: int, hotel: HotelCreateUpdateSchema) -> Hotel:
        result = await session.execute(select(Hotel).where(Hotel.hotel_id == hotel_id))
        existing_hotel = result.scalars().first()
        if not existing_hotel:
            raise HotelNotFound()

        existing_hotel.name = hotel.name
        existing_hotel.address = hotel.address
        await session.commit()
        await session.refresh(existing_hotel)
        return existing_hotel

    async def delete_hotel(self, session: AsyncSession, hotel_id: int) -> None:
        result = await session.execute(select(Hotel).where(Hotel.hotel_id == hotel_id))
        hotel = result.scalars().first()
        if not hotel:
            raise HotelNotFound()

        await session.delete(hotel)
        await session.commit()
