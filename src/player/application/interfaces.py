from abc import ABC, abstractmethod

from player.domain.entities import Player
from shared.types import PlayerId


class IPlayerQueryService(ABC):
    """
    Service for querying player information.
    """

    @abstractmethod
    def get_player(self, player_id: int):
        pass


class IPlayerService(ABC):
    """
    Service for player operations.
    """

    @abstractmethod
    def register(self, username: str, password: str) -> Player:
        pass

    @abstractmethod
    def login(self, username: str, password: str) -> Player:
        pass
