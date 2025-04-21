from fastapi import APIRouter, HTTPException, status
from project.infrastructure.postgres.repository.rooms_repo import RoomsRepository
from project.infrastructure.postgres.database import PostgresDatabase
from project.schemas.rooms import RoomSchema, RoomCreateUpdateSchema
from project.core.exceptions import RoomNotFound, RoomAlreadyExists, RoomCapacity, RoomPerPrice, ForeignKeyConstraintViolation

router = APIRouter()
rooms_repo = RoomsRepository()
database = PostgresDatabase()


@router.post(
    "/add_room",
    response_model=RoomSchema,
    status_code=status.HTTP_201_CREATED
)
async def add_room(room_dto: RoomCreateUpdateSchema) -> RoomSchema:
    async with database.session() as session:
        try:
            new_room = await rooms_repo.create_room(session=session, room=room_dto)
        except RoomCapacity as error:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error.message)
        except RoomPerPrice as error:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error.message)
        except RoomAlreadyExists as error:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=error.message)
    return new_room


@router.get(
    "/all_rooms",
    response_model=list[RoomSchema],
    status_code=status.HTTP_200_OK
)
async def get_all_rooms() -> list[RoomSchema]:
    async with database.session() as session:
        all_rooms = await rooms_repo.get_all_rooms(session=session)
        valid_rooms = [room for room in all_rooms if room.capacity >= 1]
    return valid_rooms


@router.get(
    "/room/{room_id}",
    response_model=RoomSchema,
    status_code=status.HTTP_200_OK
)
async def get_room_by_id(room_id: int) -> RoomSchema:
    async with database.session() as session:
        try:
            room = await rooms_repo.get_room_by_id(session=session, room_id=room_id)
        except RoomNotFound as error:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
    return room


@router.put(
    "/update_room/{room_id}",
    response_model=RoomSchema,
    status_code=status.HTTP_200_OK
)
async def update_room(room_id: int, room_dto: RoomCreateUpdateSchema) -> RoomSchema:
    async with database.session() as session:
        try:
            updated_room = await rooms_repo.update_room(session=session, room_id=room_id, room=room_dto)
        except RoomNotFound as error:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
        except RoomCapacity as error:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error.message)
        except RoomPerPrice as error:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error.message)
    return updated_room


@router.delete(
    "/delete_room/{room_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_room(room_id: int) -> None:
    async with database.session() as session:
        try:
            await rooms_repo.delete_room(session=session, room_id=room_id)
        except RoomNotFound as error:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
        except ForeignKeyConstraintViolation as error:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error.message)
