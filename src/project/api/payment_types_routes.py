from fastapi import APIRouter, HTTPException, status
from project.infrastructure.postgres.repository.payment_types_repo import PaymentTypesRepository
from project.infrastructure.postgres.database import PostgresDatabase
from project.schemas.payment_types import PaymentTypeSchema, PaymentTypeCreateUpdateSchema
from project.core.exceptions import PaymentTypeNotFound, PaymentTypeAlreadyExists

router = APIRouter()
payment_types_repo = PaymentTypesRepository()
database = PostgresDatabase()


@router.get(
    "/all_payment_types",
    response_model=list[PaymentTypeSchema],
    status_code=status.HTTP_200_OK
)
async def get_all_payment_types() -> list[PaymentTypeSchema]:
    async with database.session() as session:
        await payment_types_repo.check_connection(session=session)
        all_payment_types = await payment_types_repo.get_all_payment_types(session=session)
    return all_payment_types


@router.get(
    "/payment_type/{type_payment_id}",
    response_model=PaymentTypeSchema,
    status_code=status.HTTP_200_OK
)
async def get_payment_type_by_id(type_payment_id: int) -> PaymentTypeSchema:
    async with database.session() as session:
        try:
            payment_type = await payment_types_repo.get_payment_type_by_id(session=session, type_payment_id=type_payment_id)
        except PaymentTypeNotFound as error:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
    return payment_type


@router.post(
    "/add_payment_type",
    response_model=PaymentTypeSchema,
    status_code=status.HTTP_201_CREATED
)
async def add_payment_type(payment_type_dto: PaymentTypeCreateUpdateSchema) -> PaymentTypeSchema:
    async with database.session() as session:
        try:
            new_payment_type = await payment_types_repo.create_payment_type(
                session=session, payment_type=payment_type_dto
            )
        except PaymentTypeAlreadyExists as error:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Payment type already exists")
    return new_payment_type

@router.put(
    "/update_payment_type/{type_payment_id}",
    response_model=PaymentTypeSchema,
    status_code=status.HTTP_200_OK
)
async def update_payment_type(type_payment_id: int, payment_type_dto: PaymentTypeCreateUpdateSchema) -> PaymentTypeSchema:
    async with database.session() as session:
        try:
            updated_payment_type = await payment_types_repo.update_payment_type(session=session, type_payment_id=type_payment_id, payment_type=payment_type_dto)
        except PaymentTypeNotFound as error:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
    return updated_payment_type


@router.delete(
    "/delete_payment_type/{type_payment_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_payment_type(type_payment_id: int) -> None:
    async with database.session() as session:
        try:
            await payment_types_repo.delete_payment_type(session=session, type_payment_id=type_payment_id)
        except PaymentTypeNotFound as error:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
