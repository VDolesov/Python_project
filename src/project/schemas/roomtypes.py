from pydantic import BaseModel, ConfigDict, field_validator, ValidationError
from decimal import Decimal


class RoomTypeCreateUpdateSchema(BaseModel):
    hotel_id: int
    room_number: str
    room_type: str  # Убедитесь, что это поле добавлено и не является необязательным
    price_per_night: float
    capacity: int

    @field_validator("hotel_id", mode="before")
    def validate_hotel_id(cls, value):
        if value < 0:
            raise ValueError("hotel_id must be greater than or equal to 0")
        return value

    @field_validator("price_per_night", mode="before")
    def validate_price_per_night(cls, value):
        if value < 0:
            raise ValueError("price_per_night must be greater than or equal to 0")
        return value

    @field_validator("capacity", mode="before")
    def validate_capacity(cls, value):
        if value < 1:
            raise ValueError("capacity must be greater than or equal to 1")
        return value

    @field_validator("room_type", mode="before")
    def validate_room_type(cls, value):
        if not value.strip():
            raise ValueError("room_type must not be empty")
        return value


class RoomTypeSchema(RoomTypeCreateUpdateSchema):
    model_config = ConfigDict(from_attributes=True)

    room_type_id: int
