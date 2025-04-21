from pydantic import BaseModel, ConfigDict, field_validator, ValidationError
from decimal import Decimal
from datetime import date


class StayCreateUpdateSchema(BaseModel):
    room_id: int
    booking_id: int
    payment: float
    check_in_date: date
    check_out_date: date
    type_payment_id: int
    total_price: float

    @field_validator("room_id", mode="before")
    def validate_room_id(cls, value):
        if value < 0:
            raise ValueError("room_id must be greater than or equal to 0")
        return value

    @field_validator("booking_id", mode="before")
    def validate_booking_id(cls, value):
        if value < 0:
            raise ValueError("booking_id must be greater than or equal to 0")
        return value

    @field_validator("payment", "total_price")
    def validate_positive_numbers(cls, value):
        if value < 0:
            raise ValueError("Values must be greater than or equal to 0")
        return value

    @field_validator("check_out_date")
    def validate_check_out_after_check_in(cls, value, info):
        check_in_date = info.data.get("check_in_date")  # Изменение здесь
        if check_in_date and value <= check_in_date:
            raise ValueError("check_out_date must be after check_in_date")
        return value


class StaySchema(StayCreateUpdateSchema):
    model_config = ConfigDict(from_attributes=True)

    stay_id: int
