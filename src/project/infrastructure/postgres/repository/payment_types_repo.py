from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from project.infrastructure.postgres.models import PaymentType
from project.schemas.payment_types import PaymentTypeCreateUpdateSchema, PaymentTypeSchema
from project.core.exceptions import PaymentTypeNotFound, PaymentTypeAlreadyExists


class PaymentTypesRepository:
    async def check_connection(self, session: AsyncSession) -> bool:
        try:
            await session.execute(select(1))
            return True
        except Exception:
            return False

    async def get_all_payment_types(self, session: AsyncSession) -> list[PaymentTypeSchema]:
        result = await session.execute(select(PaymentType))
        return [PaymentTypeSchema.model_validate(obj=payment_type) for payment_type in result.scalars().all()]

    async def create_payment_type(self, session: AsyncSession, payment_type: PaymentTypeCreateUpdateSchema) -> PaymentType:
        existing_payment_type = await session.execute(
            select(PaymentType).where(PaymentType.name_payment == payment_type.name_payment)
        )
        if existing_payment_type.scalars().first():
            raise PaymentTypeAlreadyExists()

        new_payment_type = PaymentType(name_payment=payment_type.name_payment)
        session.add(new_payment_type)
        await session.commit()
        await session.refresh(new_payment_type)
        return new_payment_type

    async def update_payment_type(self, session: AsyncSession, type_payment_id: int, payment_type: PaymentTypeCreateUpdateSchema) -> PaymentType:
        result = await session.execute(select(PaymentType).where(PaymentType.type_payment_id == type_payment_id))
        existing_payment_type = result.scalars().first()
        if not existing_payment_type:
            raise PaymentTypeNotFound()

        existing_payment_type.name_payment = payment_type.name_payment
        await session.commit()
        await session.refresh(existing_payment_type)
        return existing_payment_type

    async def delete_payment_type(self, session: AsyncSession, type_payment_id: int) -> None:
        result = await session.execute(select(PaymentType).where(PaymentType.type_payment_id == type_payment_id))
        payment_type = result.scalars().first()
        if not payment_type:
            raise PaymentTypeNotFound()

        await session.delete(payment_type)
        await session.commit()
