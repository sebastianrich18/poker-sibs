from pydantic import BaseModel


class ChipAmount(BaseModel):
    amount: float
