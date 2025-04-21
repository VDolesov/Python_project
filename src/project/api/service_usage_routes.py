from fastapi import APIRouter, HTTPException, status
from project.infrastructure.postgres.repository.service_usage_repo import ServiceUsageRepository
from project.infrastructure.postgres.database import PostgresDatabase
from project.schemas.service_usage import ServiceUsageSchema, ServiceUsageCreateUpdateSchema
from project.core.exceptions import ServiceUsageNotFound,StayNotFound,ServiceNotFound,ServiceUsageAlreadyExists

router = APIRouter()
service_usage_repo = ServiceUsageRepository()
database = PostgresDatabase()

@router.get(
    "/all_service_usage",
    response_model=list[ServiceUsageSchema],
    status_code=status.HTTP_200_OK
)
async def get_all_service_usage() -> list[ServiceUsageSchema]:
    async with database.session() as session:
        await service_usage_repo.check_connection(session=session)
        all_usage = await service_usage_repo.get_all_service_usage(session=session)
    return all_usage


@router.get(
    "/service_usage/{usage_id}",
    response_model=ServiceUsageSchema,
    status_code=status.HTTP_200_OK
)
async def get_service_usage_by_id(usage_id: int) -> ServiceUsageSchema:
    async with database.session() as session:
        try:
            usage = await service_usage_repo.get_service_usage(session=session, usage_id=usage_id)
        except ServiceUsageNotFound as error:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
    return usage


@router.post(
    "/add_service_usage",
    response_model=ServiceUsageSchema,
    status_code=status.HTTP_201_CREATED
)
async def add_service_usage(service_usage_dto: ServiceUsageCreateUpdateSchema) -> ServiceUsageSchema:
    async with database.session() as session:
        try:
            new_service_usage = await service_usage_repo.create_service_usage(
                session=session, usage=service_usage_dto
            )
        except ValueError as error:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))
        except IntegrityError as error:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(error))
    return new_service_usage



@router.put(
    "/update_service_usage/{usage_id}",
    response_model=ServiceUsageSchema,
    status_code=status.HTTP_200_OK
)
async def update_service_usage(usage_id: int, usage_dto: ServiceUsageCreateUpdateSchema) -> ServiceUsageSchema:
    async with database.session() as session:
        try:
            updated_usage = await service_usage_repo.update_service_usage(
                session=session, usage_id=usage_id, usage=usage_dto
            )
        except ServiceUsageNotFound as error:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
    return updated_usage


@router.delete(
    "/delete_service_usage/{usage_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_service_usage(usage_id: int) -> None:
    async with database.session() as session:
        try:
            await service_usage_repo.delete_service_usage(session=session, usage_id=usage_id)
        except ServiceUsageNotFound as error:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
