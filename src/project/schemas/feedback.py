from pydantic import BaseModel, ConfigDict


class FeedbackCreateUpdateSchema(BaseModel):
    hotel_id: int
    stay_id: int
    name: str
    address: str


class FeedbackSchema(FeedbackCreateUpdateSchema):
    model_config = ConfigDict(from_attributes=True)

    feedback_id: int
