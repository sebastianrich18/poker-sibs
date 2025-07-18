from typing import Dict, List, Optional

from game.domain.value_objects import GameState

# Aggregate root for game state
class Game:
    table_id: str
    seats: Dict[int, str]  # seat_num -> player_id
    current_turn_seat: int
    game_state: GameState
