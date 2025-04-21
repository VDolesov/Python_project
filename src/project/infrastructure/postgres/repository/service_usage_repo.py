from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from project.infrastructure.postgres.models import ServiceUsage
from project.schemas.service_usage import ServiceUsageCreateUpdateSchema, ServiceUsageSchema
from project.core.exceptions import ServiceUsageNotFound

from sqlalchemy.exc import IntegrityError

class ServiceUsageRepository:
    async def check_connection(self, session: AsyncSession) -> bool:
        try:
            await session.execute(select(1))
            return True
        except Exception:
            return False

    async def get_all_service_usage(self, session: AsyncSession) -> list[ServiceUsageSchema]:
        result = await session.execute(select(ServiceUsage))
        return [ServiceUsageSchema.model_validate(obj=usage) for usage in result.scalars().all()]

    async def create_service_usage(self, session: AsyncSession, usage: ServiceUsageCreateUpdateSchema) -> ServiceUsage:
        # Проверяем, существует ли stay_id
        stay_check = await session.execute(select(1).where(ServiceUsage.stay_id == usage.stay_id))
        if not stay_check.scalar():
            raise ValueError(f"Stay with id {usage.stay_id} does not exist")

        # Проверяем, существует ли service_id
        service_check = await session.execute(select(1).where(ServiceUsage.service_id == usage.service_id))
        if not service_check.scalar():
            raise ValueError(f"Service with id {usage.service_id} does not exist")

        try:
            # Создание новой записи
            new_usage = ServiceUsage(
                stay_id=usage.stay_id,
                service_id=usage.service_id,
                quantity=usage.quantity,
                total_price=usage.total_price,
            )
            session.add(new_usage)
            await session.commit()
            await session.refresh(new_usage)
            return new_usage
        except IntegrityError as e:
            # Логируем ошибку и возвращаем клиенту понятное сообщение
            await session.rollback()
            raise ValueError(f"Integrity error: {e.orig.diag.message_detail}") from e
    async def update_service_usage(self, session: AsyncSession, usage_id: int, usage: ServiceUsageCreateUpdateSchema) -> ServiceUsage:
        result = await session.execute(select(ServiceUsage).where(ServiceUsage.service_usage_id == usage_id))
        existing_usage = result.scalars().first()
        if not existing_usage:
            raise ServiceUsageNotFound()

        existing_usage.stay_id = usage.stay_id
        existing_usage.service_id = usage.service_id
        existing_usage.quantity = usage.quantity
        existing_usage.total_price = usage.total_price
        await session.commit()
        await session.refresh(existing_usage)
        return existing_usage

    async def delete_service_usage(self, session: AsyncSession, usage_id: int) -> None:
        result = await session.execute(select(ServiceUsage).where(ServiceUsage.service_usage_id == usage_id))
        usage = result.scalars().first()
        if not usage:
            raise ServiceUsageNotFound()

        await session.delete(usage)
        await session.commit()
