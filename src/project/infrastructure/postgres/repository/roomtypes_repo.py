from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from project.infrastructure.postgres.models import RoomType
from project.schemas.roomtypes import RoomTypeCreateUpdateSchema, RoomTypeSchema
from project.core.exceptions import RoomNotFound, RoomAlreadyExists,RoomCapacity,RoomPerPrice,RoomTypeNotFound


class RoomTypesRepository:
    async def check_connection(self, session: AsyncSession) -> bool:
        try:
            await session.execute(select(1))
            return True
        except Exception:
            return False

    async def get_all_roomtypes(self, session: AsyncSession) -> list[RoomTypeSchema]:
        result = await session.execute(select(RoomType).where(RoomType.capacity >= 1))
        return [RoomTypeSchema.model_validate(obj=room_type) for room_type in result.scalars().all()]

    async def create_roomtype(self, session: AsyncSession, roomtype: RoomTypeCreateUpdateSchema) -> RoomType:
        # Проверка вместимости (capacity)
        if roomtype.capacity < 0:
            raise RoomCapacity()

        # Проверка цены (price_per_night)
        if roomtype.price_per_night <= 0:
            raise RoomPerPrice()

        # Создание нового типа комнаты
        new_roomtype = RoomType(
            hotel_id=roomtype.hotel_id,
            room_number=roomtype.room_number,
            room_type=roomtype.room_type,
            price_per_night=roomtype.price_per_night,
            capacity=roomtype.capacity,
        )
        session.add(new_roomtype)
        await session.commit()
        await session.refresh(new_roomtype)
        return new_roomtype

    async def get_all_roomtypes(self, session: AsyncSession) -> list[RoomType]:
        result = await session.execute(select(RoomType))
        return result.scalars().all()

    async def update_roomtype(self, session: AsyncSession, room_type_id: int, roomtype: RoomTypeCreateUpdateSchema) -> RoomType:
        result = await session.execute(select(RoomType).where(RoomType.room_type_id == room_type_id))
        existing_roomtype = result.scalars().first()
        if not existing_roomtype:
            raise RoomNotFound()

        existing_roomtype.hotel_id = roomtype.hotel_id
        existing_roomtype.room_number = roomtype.room_number
        existing_roomtype.room_type = roomtype.room_type
        existing_roomtype.price_per_night = roomtype.price_per_night
        existing_roomtype.capacity = roomtype.capacity
        await session.commit()
        await session.refresh(existing_roomtype)
        return existing_roomtype

    async def delete_roomtype(self, session: AsyncSession, room_type_id: int) -> None:
        result = await session.execute(select(RoomType).where(RoomType.room_type_id == room_type_id))
        room_type = result.scalars().first()

        if not room_type:
            raise RoomTypeNotFound()

        await session.delete(room_type)
        await session.commit()
