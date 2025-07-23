from abc import ABC

from game.domain.value_objects import GameAction


class GameState(ABC):
    def view_for_player(self, player_id: str) -> "GameState":
        """Return a view of the game state for the given player"""
        pass

class GameEngine(ABC):
    def validate_action(self, game_state: "GameState", player_id: str, action: GameAction) -> bool:
        """Validate if action is legal"""
        pass

    def apply_action(self, game_state: "GameState", player_id: str, action: GameAction) -> GameState:
        """Apply action to game state and return new state"""
        pass


