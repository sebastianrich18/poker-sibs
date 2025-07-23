
from game.domain.factories import GameFactory
from game.infrastructure.game_repository import GameRepository
from shared.types import PlayerId


class GameService:
    """Manages receiving and applying game actions to the game engine."""
    def __init__(self, game_repo: GameRepository, game_factory: GameFactory):
        self.game_repo = game_repo
        self.game_factory = game_factory

   