from pydantic import BaseModel

class Card(BaseModel):
    rank: str
    suit: str
