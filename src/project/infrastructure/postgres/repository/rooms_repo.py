from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from project.infrastructure.postgres.models import Room
from project.schemas.rooms import RoomCreateUpdateSchema, RoomSchema
from project.core.exceptions import RoomNotFound, RoomAlreadyExists, RoomCapacity, RoomPerPrice,ForeignKeyConstraintViolation
from sqlalchemy.exc import IntegrityError



class RoomsRepository:
    async def check_connection(self, session: AsyncSession) -> bool:
        try:
            await session.execute(select(1))
            return True
        except Exception:
            return False

    async def get_all_rooms(self, session: AsyncSession) -> list[RoomSchema]:
        result = await session.execute(select(Room).where(Room.capacity >= 1))
        return [RoomSchema.model_validate(obj=room) for room in result.scalars().all()]
    async def get_room_by_id(self, session: AsyncSession, room_id: int) -> Room:
        result = await session.execute(select(Room).where(Room.room_id == room_id))
        room = result.scalars().first()
        if not room:
            raise RoomNotFound()
        return room

    async def create_room(self, session: AsyncSession, room: RoomCreateUpdateSchema) -> Room:
        # Проверка capacity
        if room.capacity < 1:
            raise RoomCapacity()

        # Проверка price_per_night
        if room.price_per_night < 1:
            raise RoomPerPrice()

        # Проверка на существование номера
        existing_room = await session.execute(
            select(Room).where(Room.room_number == room.room_number)
        )
        if existing_room.scalars().first():
            raise RoomAlreadyExists()

        new_room = Room(
            hotel_id=room.hotel_id,
            room_type_id=room.room_type_id,
            room_number=room.room_number,
            price_per_night=room.price_per_night,
            capacity=room.capacity,
        )
        session.add(new_room)
        await session.commit()
        await session.refresh(new_room)
        return new_room

    async def update_room(self, session: AsyncSession, room_id: int, room: RoomCreateUpdateSchema) -> Room:
        result = await session.execute(select(Room).where(Room.room_id == room_id))
        existing_room = result.scalars().first()
        if not existing_room:
            raise RoomNotFound()

        # Проверка capacity
        if room.capacity < 1:
            raise RoomCapacity()

        # Проверка price_per_night
        if room.price_per_night < 1:
            raise RoomPerPrice()

        existing_room.hotel_id = room.hotel_id
        existing_room.room_type_id = room.room_type_id
        existing_room.room_number = room.room_number
        existing_room.price_per_night = room.price_per_night
        existing_room.capacity = room.capacity

        await session.commit()
        await session.refresh(existing_room)
        return existing_room

    async def delete_room(self, session: AsyncSession, room_id: int) -> None:
        result = await session.execute(select(Room).where(Room.room_id == room_id))
        room = result.scalars().first()
        if not room:
            raise RoomNotFound()

        try:
            await session.delete(room)
            await session.commit()
        except IntegrityError as exc:
            raise ForeignKeyConstraintViolation(
                f"Unable to delete room with ID {room_id} because it is referenced by another record."
            ) from exc