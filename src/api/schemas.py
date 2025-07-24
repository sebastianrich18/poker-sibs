from typing import List
from pydantic import BaseModel

from shared.types import PlayerId


class LoginPlayerRequest(BaseModel):
    username: str
    password: str


class LoginPlayerResponse(BaseModel):
    access_token: str
    token_type: str


class CreatePlayerRequest(BaseModel):
    username: str
    password: str
    email: str


class CreatePlayerResponse(BaseModel):
    access_token: str
    token_type: str


class GetPlayerResponse(BaseModel):
    player_id: PlayerId
    username: str
    email: str
    is_active: bool


class GetTableResponse(BaseModel):
    table_id: str
    name: str
    players: List[str]
    stakes: str
    status: str
