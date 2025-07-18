from pydantic import BaseModel


class ChipAmount(BaseModel):
    amount: float

class LedgerEntry(BaseModel):
    user_id: str
    change: float
    reason: str

