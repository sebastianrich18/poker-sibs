from pydantic import BaseModel
from shared.types import PlayerId


class Player(BaseModel):
    player_id: PlayerId
    username: str
    password_hash: str
