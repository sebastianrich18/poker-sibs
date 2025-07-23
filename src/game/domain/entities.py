from typing import Dict, List, Optional

from game.domain.exceptions import NoSeatsAvaliableError, PlayerNotFoundError
from game.domain.interfaces import GameEngine, GameState
from game.domain.value_objects import GameAction
from shared.types import PlayerId

class Game:
    table_id: str
    seats: Dict[int, PlayerId]  # seat_num -> player_id
    current_turn_seat: int

    game_state: GameState
    game_engine: GameEngine

    def validate_action(self, player_id: PlayerId, action: GameAction) -> bool:
        """Validate if action is legal"""
        return self.game_engine.validate_action(self.game_state, player_id, action)

    def apply_action(self, player_id: PlayerId, action: GameAction) -> GameState:
        """Apply action to game state and return new state"""
        self.game_state = self.game_engine.apply_action(
            self.game_state, player_id, action
        )
        return self.game_state

    def view_state_for_player(self, player_id: PlayerId) -> GameState:
        """Return a view of the game state for the given player"""
        return self.game_state.view_for_player(player_id)

    def is_full(self) -> bool:
        """Check if game is full"""
        for seat in range(self.max_seats):
            if seat not in self.seats:
                return False
        return True

    def seat_player(self, player_id: PlayerId) -> bool:
        """Add player to table if space available"""
        if self.is_full():
            raise NoSeatsAvaliableError("Game has no open seats")
        for seat in range(self.max_seats):
            if seat not in self.seats:
                self.seats[seat] = player_id
                return True
        return False

    def remove_player(self, player_id: PlayerId) -> bool:
        """Remove player from table"""
        for seat, pid in self.seats.items():
            if pid == player_id:
                del self.seats[seat]
                return True
        raise PlayerNotFoundError("Player is not in this game")
