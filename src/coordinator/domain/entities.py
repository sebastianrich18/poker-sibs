from pydantic import BaseModel
from typing import Optional
from ...core.domain.entities import EntityId


class LoginRequest(BaseModel):
    username: str
    password: str


class CreateAccountRequest(BaseModel):
    username: str
    password: str


class LobbyJoinRequest(BaseModel):
    user_id: EntityId


class LeaveRequest(BaseModel):
    chips: int
