from fastapi import APIRouter, HTTPException, status
from project.infrastructure.postgres.repository.roomtypes_repo import RoomTypesRepository
from project.infrastructure.postgres.database import PostgresDatabase
from project.schemas.roomtypes import RoomTypeSchema, RoomTypeCreateUpdateSchema
from project.core.exceptions import RoomPerPrice, RoomAlreadyExists, HotelNotFound,RoomCapacity

router = APIRouter()
roomtypes_repo = RoomTypesRepository()
database = PostgresDatabase()


@router.post(
    "/add_roomtype",
    response_model=RoomTypeSchema,
    status_code=status.HTTP_201_CREATED
)
async def add_roomtype(roomtype_dto: RoomTypeCreateUpdateSchema) -> RoomTypeSchema:
    async with database.session() as session:
        try:
            new_roomtype = await roomtypes_repo.create_roomtype(session=session, roomtype=roomtype_dto)
        except RoomCapacity as error:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error.message)
        except RoomPerPrice as error:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error.message)
        except RoomAlreadyExists as error:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=error.message)
        except HotelNotFound as error:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
    return new_roomtype


@router.get(
    "/all_roomtypes",
    response_model=list[RoomTypeSchema],
    status_code=status.HTTP_200_OK
)
async def get_all_roomtypes() -> list[RoomTypeSchema]:
    async with database.session() as session:
        all_roomtypes = await roomtypes_repo.get_all_roomtypes(session=session)
    return all_roomtypes


@router.get(
    "/roomtype/{room_type_id}",
    response_model=RoomTypeSchema,
    status_code=status.HTTP_200_OK
)
async def get_roomtype_by_id(room_type_id: int) -> RoomTypeSchema:
    async with database.session() as session:
        try:
            roomtype = await roomtypes_repo.get_roomtype_by_id(session=session, room_type_id=room_type_id)
        except RoomAlreadyExists as error:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
    return roomtype


@router.put(
    "/update_roomtype/{room_type_id}",
    response_model=RoomTypeSchema,
    status_code=status.HTTP_200_OK
)
async def update_roomtype(room_type_id: int, roomtype_dto: RoomTypeCreateUpdateSchema) -> RoomTypeSchema:
    async with database.session() as session:
        try:
            updated_roomtype = await roomtypes_repo.update_roomtype(session=session, room_type_id=room_type_id, roomtype=roomtype_dto)
        except RoomCapacity as error:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error.message)
        except RoomPerPrice as error:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error.message)
        except RoomAlreadyExists as error:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=error.message)
        except HotelNotFound as error:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
    return updated_roomtype


@router.delete(
    "/delete_roomtype/{room_type_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_roomtype(room_type_id: int) -> None:
    async with database.session() as session:
        try:
            await roomtypes_repo.delete_roomtype(session=session, room_type_id=room_type_id)
        except RoomAlreadyExists as error:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
