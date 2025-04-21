from pydantic import BaseModel, ConfigDict, field_validator, ValidationError
from decimal import Decimal


class ServiceCreateUpdateSchema(BaseModel):
    service_name: str
    price: float

    @field_validator("price", mode="before")
    def validate_price(cls, value):
        if value < 0:
            raise ValueError("price must be greater than or equal to 0")
        return value


class ServiceSchema(ServiceCreateUpdateSchema):
    model_config = ConfigDict(from_attributes=True)

    service_id: int
