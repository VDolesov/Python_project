from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from project.infrastructure.postgres.models import Client
from project.schemas.clients import ClientCreateUpdateSchema, ClientSchema
from project.core.exceptions import ClientNotFound, ClientAlreadyExists


class ClientsRepository:
    async def check_connection(self, session: AsyncSession) -> bool:
        try:
            await session.execute(select(1))
            return True
        except Exception:
            return False

    async def get_all_clients(self, session: AsyncSession) -> list[ClientSchema]:
        result = await session.execute(select(Client))

        return [ClientSchema.model_validate(obj=client) for client in result.scalars().all()]

    async def get_client(self, session: AsyncSession, client_id: int) -> ClientSchema:
        result = await session.execute(select(Client).where(Client.client_id == client_id))
        client = result.scalars().first()
        if not client:
            raise ClientNotFound()
        return ClientSchema.model_validate(obj=client)
    async def create_client(self, session: AsyncSession, client: ClientCreateUpdateSchema) -> Client:
        existing_client = await session.execute(
            select(Client).where(Client.email == client.email)
        )
        if existing_client.scalars().first():
            raise ClientAlreadyExists()

        new_client = Client(full_name=client.full_name, phone_number=client.phone_number, email=client.email)
        session.add(new_client)
        await session.commit()
        await session.refresh(new_client)
        return new_client

    async def update_client(self, session: AsyncSession, client_id: int, client: ClientCreateUpdateSchema) -> Client:
        result = await session.execute(select(Client).where(Client.client_id == client_id))
        existing_client = result.scalars().first()
        if not existing_client:
            raise ClientNotFound()

        existing_client.full_name = client.full_name
        existing_client.phone_number = client.phone_number
        existing_client.email = client.email
        await session.commit()
        await session.refresh(existing_client)
        return existing_client

    async def delete_client(self, session: AsyncSession, client_id: int) -> None:
        result = await session.execute(select(Client).where(Client.client_id == client_id))
        client = result.scalars().first()
        if not client:
            raise ClientNotFound()

        await session.delete(client)
        await session.commit()
