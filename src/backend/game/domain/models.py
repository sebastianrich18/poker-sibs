from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional


class BettingRound(str, Enum):
    PREFLOP = "PREFLOP"
    FLOP = "FLOP"
    TURN = "TURN"
    RIVER = "RIVER"


@dataclass
class Card:
    rank: str
    suit: str


@dataclass
class PlayerAction:
    player_id: str
    action: str
    amount: Optional[int] = None


@dataclass
class HandState:
    hand_id: str
    players: List[str]
    player_cards: Dict[str, List[Card]] = field(default_factory=dict)
    community_cards: List[Card] = field(default_factory=list)
    pot: int = 0
    current_round: BettingRound = BettingRound.PREFLOP
    action_on: Optional[str] = None
    last_aggressor: Optional[str] = None
    betting_history: List[PlayerAction] = field(default_factory=list)

    def apply_action(self, player_id: str, action: PlayerAction) -> "ActionResult":
        # Placeholder validation logic
        self.betting_history.append(action)
        self.action_on = player_id
        return ActionResult(success=True, error_reason=None, new_state=None)

    def is_complete(self) -> bool:
        # Placeholder completion check
        return False


@dataclass
class PokerGame:
    table_id: str
    seats: Dict[int, Optional[str]] = field(default_factory=dict)
    stacks: Dict[str, int] = field(default_factory=dict)
    current_hand: Optional[HandState] = None
    dealer_button: int = 0

    def add_player(self, player_id: str, seat: int, chips: int) -> None:
        if seat in self.seats and self.seats[seat] is not None:
            raise ValueError("Seat already occupied")
        self.seats[seat] = player_id
        self.stacks[player_id] = chips

    def remove_player(self, player_id: str) -> int:
        seat = None
        for s, pid in self.seats.items():
            if pid == player_id:
                seat = s
                break
        if seat is not None:
            self.seats[seat] = None
        final_stack = self.stacks.pop(player_id, 0)
        return final_stack

    def can_start_hand(self) -> bool:
        players = [p for p in self.seats.values() if p]
        return len(players) >= 2

    def start_new_hand(self, shuffle_seed: str) -> HandState:
        self.current_hand = HandState(hand_id=f"hand-{datetime.utcnow().isoformat()}", players=[p for p in self.seats.values() if p])
        return self.current_hand


@dataclass
class CompletedHand:
    hand_id: str
    table_id: str
    players: List[str]
    all_actions: List[str]
    community_cards: List[str]
    winners: List[str]
    pot_distribution: Dict[str, int]
    rake: int
    shuffle_seed: str
    completed_at: datetime


@dataclass
class AvailableAction:
    type: str
    amount: Optional[int] = None


@dataclass
class PlayerInfo:
    player_id: str
    seat: int
    stack: int


@dataclass
class GameState:
    table_id: str
    seats: Dict[int, Optional[PlayerInfo]]
    community_cards: List[str]
    pot: int
    current_round: str
    action_on: Optional[str]
    available_actions: List[AvailableAction]
    my_cards: Optional[List[str]]


@dataclass
class ActionResult:
    success: bool
    error_reason: Optional[str]
    new_state: Optional[GameState]
