from game.application.game_service import GameService
from game.domain.exceptions import NoOpenSeatsError
from player.domain.entities import PlayerId
from table.domain.entities import TableId
from table.domain.exceptions import NoOpenSeatsAtTableError


class TableService:
    def __init__(self, game_service: GameService):
        self.game_service = game_service

    def join_table(self, table_id: TableId, player_id: PlayerId) -> bool:
        """Add player to table if space available"""
        # check balance
        # reserve chips

        try:
            self.game_service.seat_player(player_id)
        except NoOpenSeatsError:
            # release chips
            raise
        return True

    def leave_table(self, table_id: TableId, player_id: PlayerId) -> bool:
        """Remove player from table"""
        self.game_service.remove_player(player_id)
        return True
