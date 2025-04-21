from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from project.infrastructure.postgres.models import Service
from project.schemas.services import ServiceCreateUpdateSchema, ServiceSchema
from project.core.exceptions import ServiceNotFound, ServiceAlreadyExists, InvalidServicePrice


class ServicesRepository:
    async def check_connection(self, session: AsyncSession) -> bool:
        try:
            await session.execute(select(1))
            return True
        except Exception:
            return False


    async def get_service_by_id(self, session: AsyncSession, service_id: int) -> Service:
        try:
            query = await session.get(Service, service_id)
            if query is None:
                raise ServiceNotFound(f"Service with id {service_id} not found.")
            return query
        except NoResultFound:
            raise ServiceNotFound(f"Service with id {service_id} not found.")
    async def get_all_services(self, session: AsyncSession) -> list[ServiceSchema]:
        result = await session.execute(select(Service))
        return [ServiceSchema.model_validate(obj=service) for service in result.scalars().all()]

    async def create_service(self, session: AsyncSession, service: ServiceCreateUpdateSchema) -> Service:
        # Проверка на уникальность service_name
        service_check = await session.execute(
            select(Service).where(Service.service_name == service.service_name)
        )
        if service_check.scalars().first():
            raise ServiceAlreadyExists()

        # Проверка, что цена больше 0
        if service.price <= 0:
            raise InvalidServicePrice()

        # Создание новой записи
        new_service = Service(service_name=service.service_name, price=service.price)
        session.add(new_service)
        await session.commit()
        await session.refresh(new_service)
        return new_service

    async def update_service(self, session: AsyncSession, service_id: int, service: ServiceCreateUpdateSchema) -> Service:
        result = await session.execute(select(Service).where(Service.service_id == service_id))
        existing_service = result.scalars().first()
        if not existing_service:
            raise ServiceNotFound()

        existing_service.service_name = service.service_name
        existing_service.price = service.price
        await session.commit()
        await session.refresh(existing_service)
        return existing_service

    async def delete_service(self, session: AsyncSession, service_id: int) -> None:
        result = await session.execute(select(Service).where(Service.service_id == service_id))
        service = result.scalars().first()
        if not service:
            raise ServiceNotFound()

        await session.delete(service)
        await session.commit()
