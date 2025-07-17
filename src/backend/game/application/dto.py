from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional

from ..domain.models import PlayerInfo, AvailableAction


@dataclass
class GameState:
    """Complete game state for UI rendering"""
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


@dataclass
class PlayerHandInfo:
    player_id: str
    cards: List[str]
    final_stack: int


@dataclass
class CompletedHand:
    """Persisted after hand completion"""
    hand_id: str
    table_id: str
    players: List[PlayerHandInfo]
    all_actions: List[str]
    community_cards: List[str]
    winners: List[str]
    pot_distribution: Dict[str, int]
    rake: int
    shuffle_seed: str
    completed_at: datetime
