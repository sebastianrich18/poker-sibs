from game.domain.entities import Game
from game.domain.enums import GameType


class GameFactory:
    """Factory to create new game instances."""

    @staticmethod
    def create_game(self, max_seats: int, game_type: GameType) -> Game:
        pass
