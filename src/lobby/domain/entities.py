from pydantic import BaseModel
from typing import Dict, Optional

class JoinAck(BaseModel):
    userId: str
    seat: int

class ErrorMessage(BaseModel):
    error: str

class PlayerJoined(BaseModel):
    userId: str
    seat: int

class PlayerLeft(BaseModel):
    userId: str

class Card(BaseModel):
    rank: str
    suit: str

class Action(BaseModel):
    action: str
    amount: Optional[int] = None

class ActionBroadcast(Action):
    userId: str

class RoundResult(BaseModel):
    results: Dict[str, int]
