from abc import ABC


class GameEngine(ABC):
    pass


class GameState(ABC):

    def view_for_player(self, player_id: str) -> "GameState":
        """Return a view of the game state for the given player"""
        pass
