
from abc import ABC, abstractmethod

class PlayerQueryService(ABC):
    """
    Service for querying player information.
    """
    @abstractmethod
    def get_player(self, player_id: int):
        pass