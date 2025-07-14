from pydantic import BaseModel, Field
from typing import List, NewType

EntityId = NewType("EntityId", str)


class User(BaseModel):
    id: EntityId
    username: str
    hashed_password: str
    chips: int = 1000
    in_lobby: bool = False


class Lobby(BaseModel):
    id: EntityId
    name: str
    max_players: int = 9
    players: List[EntityId] = Field(default_factory=list)
    status: str = "waiting"
