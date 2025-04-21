from pydantic import BaseModel, ConfigDict


class HotelCreateUpdateSchema(BaseModel):
    name: str
    address: str | None = None


class HotelSchema(HotelCreateUpdateSchema):
    model_config = ConfigDict(from_attributes=True)

    hotel_id: int
