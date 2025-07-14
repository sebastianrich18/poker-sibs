import uuid
from pydantic import BaseModel



class EntityId(BaseModel):
    id: uuid.UUID

    def __str__(self):
        return f"EntityId(id={self.id})"

class UserId(EntityId):
    def __str__(self):
        return f"UserId(id={self.id})"
    
class LobbyId(EntityId):
    def __str__(self):
        return f"LobbyId(id={self.id})"

class User(BaseModel):
    id: UserId
    username: str
    chip_balance: float
    in_lobby: bool = False

    def __str__(self):
        return f"User(id={self.id}, username='{self.username}', chip_balance={self.chip_balance}, in_lobby={self.in_lobby})"
    

class Lobby(BaseModel):
    id: LobbyId
    name: str
    max_players: int
    current_players: int = 0

    def __str__(self):
        return f"Lobby(id={self.id}, name='{self.name}', max_players={self.max_players}, current_players={self.current_players})"
    



