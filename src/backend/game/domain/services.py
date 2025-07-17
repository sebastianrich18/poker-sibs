from typing import Dict, List

from .models import HandState, Card, PlayerAction


class PokerRulesEngine:
    @staticmethod
    def validate_action(state: HandState, player_id: str, action: PlayerAction) -> bool:
        # Placeholder: always return True for now
        return True

    @staticmethod
    def determine_winners(state: HandState) -> List[str]:
        # Placeholder: split pot among all players still in hand
        return state.players

    @staticmethod
    def calculate_payouts(pot: int, winners: List[str]) -> Dict[str, int]:
        share = pot // len(winners)
        return {w: share for w in winners}


class IRandomnessProvider:
    async def generate_seed(self) -> str:
        raise NotImplementedError

    async def shuffle(self, items: List[any], seed: str) -> List[any]:
        raise NotImplementedError


class DeckService:
    def __init__(self, randomness: IRandomnessProvider):
        self.randomness = randomness

    async def create_shuffled_deck(self, seed: str) -> List[Card]:
        ranks = ["A", "K", "Q", "J"] + [str(n) for n in range(10, 1, -1)]
        suits = ["h", "d", "c", "s"]
        deck = [Card(rank=r, suit=s) for s in suits for r in ranks]
        return await self.randomness.shuffle(deck, seed)
