from pydantic import BaseModel
from typing import Dict, Optional
from ...core.domain.entities import EntityId
from ...poker.domain.entities import Card, ActionType


class JoinAck(BaseModel):
    userId: EntityId
    seat: int


class ErrorMessage(BaseModel):
    error: str


class PlayerJoined(BaseModel):
    userId: EntityId
    seat: int


class PlayerLeft(BaseModel):
    userId: EntityId


class Action(BaseModel):
    action: ActionType
    amount: Optional[int] = None


class ActionBroadcast(Action):
    userId: EntityId


class RoundResult(BaseModel):
    results: Dict[str, int]
