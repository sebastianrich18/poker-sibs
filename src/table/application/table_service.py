from game.application.game_service import GameService
from shared.types import TableId, PlayerId


class TableService:
    def __init__(self, game_service: GameService):
        self.game_service = game_service

    def join_table(self, table_id: TableId, player_id: PlayerId) -> bool:
        """Add player to table if space available"""
        # check balance
        # reserve chips

        try:
            self.game_service.seat_player(player_id)
        except NoSeatsAvaliableError:
            # release chips
            raise
        return True

    def leave_table(self, table_id: TableId, player_id: PlayerId) -> bool:
        """Remove player from table"""
        self.game_service.remove_player(player_id)
        return True
