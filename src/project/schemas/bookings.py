from pydantic import BaseModel, validator, ConfigDict, field_validator, ValidationError
from datetime import date


class BookingCreateUpdateSchema(BaseModel):
    client_id: int
    room_type_id: int
    hotel_id: int
    booking_date: date
    check_in_date: date
    check_out_date: date

    @field_validator("client_id", mode="before")
    def validate_client_id(cls, value):
        if value < 0:
            raise ValueError("client_id must be greater than to 0")
        return value

    @field_validator("room_type_id", mode="before")
    def validate_room_type_id(cls, value):
        if value < 0:
            raise ValueError(" room_type_id must be greater than or equal to 0")
        return value

    @field_validator("hotel_id", mode="before")
    def validate_hotel_id(cls, value):
        if value < 0:
            raise ValueError("hotel_id must be greater than or equal to 0")
        return value

class BookingSchema(BookingCreateUpdateSchema):
    model_config = ConfigDict(from_attributes=True)

    booking_id: int
