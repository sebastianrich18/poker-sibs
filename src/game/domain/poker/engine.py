from typing import Dict, List
from game.domain.interfaces import IGameEngine
from game.domain.poker.enums import Action
from game.domain.poker.value_objects import PokerGameState
from game.infrastructure.randomness_provider import IRandomnessProvider


class PokerRulesEngine(IGameEngine):
    @staticmethod
    def validate_action(state: PokerGameState, player_id: str, action: Action) -> bool:
        """Validate if action is legal"""

    @staticmethod
    def determine_winners(state: PokerGameState) -> List[str]:
        """Determine winner(s) of hand"""

    @staticmethod
    def calculate_payouts(pot: int, winners: List[str]) -> Dict[str, int]:
        """Calculate pot distribution"""

    @staticmethod
    def apply_action(
        state: PokerGameState, player_id: str, action: Action
    ) -> PokerGameState:
        """Apply action to hand state and return new state"""


class DeckService:
    def __init__(self, randomness: IRandomnessProvider):
        pass

    async def create_shuffled_deck(self, seed: str) -> List[str]:
        """Create deterministically shuffled deck"""
