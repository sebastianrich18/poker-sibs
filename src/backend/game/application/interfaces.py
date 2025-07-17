from abc import ABC, abstractmethod
from typing import Optional

from .dto import GameState, ActionResult


class IGameService(ABC):
    @abstractmethod
    async def start_round_if_ready(self, table_id: str) -> Optional[str]:
        """Start new hand if conditions met and return hand_id."""

    @abstractmethod
    async def process_player_action(self, table_id: str, player_id: str, action: dict) -> ActionResult:
        """Process game action."""

    @abstractmethod
    async def get_current_state(self, table_id: str, player_id: str) -> GameState:
        """Get game state from player perspective."""

    @abstractmethod
    async def add_player(self, table_id: str, player_id: str, buy_in: int) -> None:
        """Add player to game."""

    @abstractmethod
    async def remove_player(self, table_id: str, player_id: str) -> int:
        """Remove player and return final stack."""


class IHandHistoryRepository(ABC):
    @abstractmethod
    async def save_completed_hand(self, hand):
        """Persist completed hand for audit."""
