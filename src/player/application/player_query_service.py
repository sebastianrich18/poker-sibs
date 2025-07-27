import json
import os
from player.application.interfaces import IPlayerQueryService


class FileSystemPlayerQueryService(IPlayerQueryService):
    """
    Implementation of PlayerQueryService for file system storage.
    """

    def __init__(self, file_path="players.json"):
        self.file_path = file_path
        if not os.path.exists(file_path):
            with open(file_path, "w") as f:
                f.write("[]")

    def get_player(self, player_id: int):
        """
        Retrieve player information by player ID.
        """
        with open(self.file_path, "r") as f:
            players = json.load(f)
            for player in players:
                if player["player_id"] == player_id:
                    return player
        raise ValueError(f"Player with ID {player_id} not found.")


class PostgressPlayerQueryService(IPlayerQueryService):
    """
    Implementation of PlayerQueryService for PostgreSQL.
    """

    def __init__(self, db_session):
        self.db_session = db_session

    def get_player(self, player_id: int):
        """
        Retrieve player information by player ID.
        """
        # Placeholder for actual database query logic
        return {"player_id": player_id, "name": "Player Name", "status": "active"}
