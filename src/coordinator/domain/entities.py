from pydantic import BaseModel
from typing import Optional

class LoginRequest(BaseModel):
    username: str
    password: str

class CreateAccountRequest(BaseModel):
    username: str
    password: str

class LobbyJoinRequest(BaseModel):
    user_id: str

class LeaveRequest(BaseModel):
    chips: int
