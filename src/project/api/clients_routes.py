from fastapi import APIRouter, HTTPException, status, Query

from project.infrastructure.postgres.repository.clients_repo import ClientsRepository
from project.infrastructure.postgres.database import PostgresDatabase
from project.schemas.clients import ClientSchema, ClientCreateUpdateSchema
from project.core.exceptions import ClientNotFound, ClientAlreadyExists

router = APIRouter()
clients_repo = ClientsRepository()
database = PostgresDatabase()


@router.get(
    "/all_clients",
    response_model=list[ClientSchema],
    status_code=status.HTTP_200_OK
)
async def get_all_clients() -> list[ClientSchema]:
    async with database.session() as session:
        await clients_repo.check_connection(session=session)
        all_clients = await clients_repo.get_all_clients(session=session)
    return all_clients


@router.get(
    "/client/{client_id}",
    response_model=ClientSchema,
    status_code=status.HTTP_200_OK
)
async def get_client_by_id(client_id: int) -> ClientSchema:
    async with database.session() as session:
        try:
            client = await clients_repo.get_client(session=session, client_id=client_id)
        except ClientNotFound as error:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
    return client



@router.post(
    "/add_client",
    response_model=ClientSchema,
    status_code=status.HTTP_201_CREATED
)
async def add_client(client_dto: ClientCreateUpdateSchema) -> ClientSchema:
    async with database.session() as session:
        try:
            new_client = await clients_repo.create_client(session=session, client=client_dto)
        except ClientAlreadyExists as error:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=error.message)
    return new_client


@router.put(
    "/update_client/{client_id}",
    response_model=ClientSchema,
    status_code=status.HTTP_200_OK
)
async def update_client(client_id: int, client_dto: ClientCreateUpdateSchema) -> ClientSchema:
    async with database.session() as session:
        try:
            updated_client = await clients_repo.update_client(session=session, client_id=client_id, client=client_dto)
        except ClientNotFound as error:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
    return updated_client


@router.delete(
    "/delete_client/{client_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_client(client_id: int) -> None:
    async with database.session() as session:
        try:
            await clients_repo.delete_client(session=session, client_id=client_id)
        except ClientNotFound as error:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
