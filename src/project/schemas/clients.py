from pydantic import BaseModel, ConfigDict, EmailStr


class ClientCreateUpdateSchema(BaseModel):
    full_name: str
    phone_number: str | None = None
    email: EmailStr | None = None


class ClientSchema(ClientCreateUpdateSchema):
    model_config = ConfigDict(from_attributes=True)

    client_id: int
