from pydantic import BaseModel, ConfigDict, field_validator, ValidationError

class RoomCreateUpdateSchema(BaseModel):
    hotel_id: int
    room_type_id: int
    room_number: str
    price_per_night: float
    capacity: int

    @field_validator("hotel_id", mode="before")
    def validate_hotel_id(cls, value):
        if value < 0:
            raise ValueError("hotel_id must be greater than to 0")
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


class RoomSchema(RoomCreateUpdateSchema):
    model_config = ConfigDict(from_attributes=True)

    room_id: int
