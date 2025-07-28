from typing import Optional
from uuid import uuid4
from player.application.interfaces import IPlayerService
from player.domain.entities import Player
from player.infrastructure.hashing_service import HashingService
from player.infrastructure.player_repository import (
    FileSystemPlayerRepository,
    IPlayerRepository,
)


class PlayerService(IPlayerService):
    def __init__(self):
        self.player_repository: IPlayerRepository = FileSystemPlayerRepository(
            "players.json"
        )

    def register(self, username: str, password: str) -> Player:
        """
        Create a new player with the provided data.
        """
        username_exists = True
        try:
            self.player_repository.get_player_by_username(username)
        except ValueError:
            username_exists = False
        if username_exists:
            raise ValueError("Username already exists.")
        
        player = Player(
            player_id=uuid4(),
            username=username,
            password_hash=HashingService.hash(password),
        )
        return self.player_repository.create_player(player)

    def login(self, username: str, password: str) -> Optional[Player]:
        """
        Authenticate a player with the provided username and password.
        """
        try:
            player = self.player_repository.get_player_by_username(username)
            if player and HashingService.verify(player.password_hash, password):
                return player
        except ValueError:
            raise ValueError("Invalid username or password")
