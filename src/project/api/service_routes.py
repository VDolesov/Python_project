from fastapi import APIRouter, HTTPException, status
from project.infrastructure.postgres.repository.services_repo import ServicesRepository
from project.infrastructure.postgres.database import PostgresDatabase
from project.schemas.services import ServiceSchema, ServiceCreateUpdateSchema
from project.core.exceptions import ServiceNotFound, ServiceAlreadyExists,InvalidServicePrice

router = APIRouter()
services_repo = ServicesRepository()
database = PostgresDatabase()

@router.get(
    "/all_services",
    response_model=list[ServiceSchema],
    status_code=status.HTTP_200_OK
)
async def get_all_services() -> list[ServiceSchema]:
    async with database.session() as session:
        await services_repo.check_connection(session=session)
        all_services = await services_repo.get_all_services(session=session)
    return all_services


@router.get(
    "/service/{service_id}",
    response_model=ServiceSchema,
    status_code=status.HTTP_200_OK
)
async def get_service_by_id(service_id: int) -> ServiceSchema:
    async with database.session() as session:
        try:
            service = await services_repo.get_service_by_id(session=session, service_id=service_id)
        except ServiceNotFound as error:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
    return service


@router.post(
    "/add_service",
    response_model=ServiceSchema,
    status_code=status.HTTP_201_CREATED
)
async def add_service(service_dto: ServiceCreateUpdateSchema) -> ServiceSchema:
    async with database.session() as session:
        try:
            new_service = await services_repo.create_service(session=session, service=service_dto)
        except InvalidServicePrice as error:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error.message)
        except ServiceAlreadyExists as error:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=error.message)
    return new_service

@router.put(
    "/update_service/{service_id}",
    response_model=ServiceSchema,
    status_code=status.HTTP_200_OK
)
async def update_service(service_id: int, service_dto: ServiceCreateUpdateSchema) -> ServiceSchema:
    async with database.session() as session:
        try:
            updated_service = await services_repo.update_service(
                session=session, service_id=service_id, service=service_dto
            )
        except ServiceNotFound as error:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
    return updated_service


@router.delete(
    "/delete_service/{service_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_service(service_id: int) -> None:
    async with database.session() as session:
        try:
            await services_repo.delete_service(session=session, service_id=service_id)
        except ServiceNotFound as error:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
