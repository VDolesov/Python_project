from pydantic import BaseModel, ConfigDict


class PaymentTypeCreateUpdateSchema(BaseModel):
    name_payment: str


class PaymentTypeSchema(PaymentTypeCreateUpdateSchema):
    model_config = ConfigDict(from_attributes=True)

    type_payment_id: int
