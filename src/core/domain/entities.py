from pydantic import BaseModel, Field
from typing import List

class User(BaseModel):
    id: str
    username: str
    hashed_password: str
    chips: int = 1000
    in_lobby: bool = False

class Lobby(BaseModel):
    id: str
    name: str
    max_players: int = 9
    players: List[str] = Field(default_factory=list)
    status: str = "waiting"
