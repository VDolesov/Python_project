from pydantic import BaseModel, ConfigDict, field_validator, ValidationError
from decimal import Decimal


class ServiceUsageCreateUpdateSchema(BaseModel):
    stay_id: int
    service_id: int
    quantity: int
    total_price: float


    @field_validator("stay_id", mode="before")
    def validate_stay_id(cls, value):
        if value <= 0:
            raise ValueError("stay_id must be greater than 0")
        return value

    @field_validator("service_id", mode="before")
    def validate_service_id(cls, value):
        if value <= 0:
            raise ValueError("service_id must be greater than 0")
        return value

    @field_validator("quantity", mode="before")
    def validate_quantity(cls, value):
        if value <= 0:
            raise ValueError("quantity must be greater than 0")
        return value

    @field_validator("total_price", mode="before")
    def validate_total_price(cls, value):
        if value < 0:
            raise ValueError("total_price must be greater than or equal to 0")
        return value

class ServiceUsageSchema(ServiceUsageCreateUpdateSchema):
    model_config = ConfigDict(from_attributes=True)

    service_usage_id: int
