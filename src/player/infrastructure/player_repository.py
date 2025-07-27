from abc import ABC, abstractmethod
import json
import os
from player.domain.entities import Player
from shared.types import PlayerId


class IPlayerRepository(ABC):
    """
    Repository interface for player operations.
    """

    @abstractmethod
    def get_player_by_id(self, player_id: PlayerId) -> Player:
        """
        Retrieve a player by their ID.
        """
        pass

    @abstractmethod
    def get_player_by_username(self, username: str) -> Player:
        """
        Retrieve a player by their username.
        """
        pass

    @abstractmethod
    def create_player(self, player: Player) -> Player:
        """
        Create a new player.
        """
        pass

    @abstractmethod
    def update_player(self, player: Player) -> Player:
        """
        Update an existing player's information.
        """
        pass

    @abstractmethod
    def delete_player(self, player_id: PlayerId):
        """
        Delete a player by their ID.
        """
        pass


class FileSystemPlayerRepository(IPlayerRepository):
    """
    File system implementation of the player repository.
    """

    def __init__(self, file_path: str):
        self.file_path = file_path
        if not os.path.exists(file_path):
            with open(file_path, "w") as f:
                f.write("[]")

    def get_player_by_id(self, player_id: PlayerId) -> Player:
        with open(self.file_path, "r") as f:
            players = json.load(f)
            for player in players:
                if player["player_id"] == player_id:
                    player["player_id"] = str(player["player_id"])  # Ensure UUID is a string
                    return Player(**player)
        raise ValueError(f"Player with ID {player_id} not found.")

    def get_player_by_username(self, username: str) -> Player:
        with open(self.file_path, "r") as f:
            players = json.load(f)
            for player in players:
                if player["username"] == username:
                    return Player(**player)
        raise ValueError(f"Player with username {username} not found.")

    def create_player(self, player: Player) -> None:
        player.player_id = str(player.player_id)  # Ensure UUID is a string
        with open(self.file_path, "r+") as f:
            players = json.load(f)
            players.append(player.model_dump())
            f.seek(0)
            json.dump(players, f)
        return player

    def update_player(self, player: Player) -> None:
        with open(self.file_path, "r+") as f:
            players = json.load(f)
            for i, p in enumerate(players):
                if p["player_id"] == player.player_id:
                    players[i] = player.model_dump()
                    f.seek(0)
                    json.dump(players, f)
        raise ValueError(f"Player with ID {player.player_id} not found.")

    def delete_player(self, player_id: PlayerId):
        with open(self.file_path, "r+") as f:
            players = json.load(f)
            players = [p for p in players if p["player_id"] != player_id]
            f.seek(0)
            f.truncate()
            json.dump(players, f)
        raise ValueError(f"Player with ID {player_id} not found.")
