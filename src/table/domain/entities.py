from game.domain.entities import Game
from player.domain.entities import PlayerId
from table.domain.exceptions import NoOpenSeatsAtTableError, PlayerNotAtTableError


class TableId:
    pass


class Table:
    id: TableId
    game: Game
    max_seats: int
    seats: dict[int, PlayerId]  # seat_num -> player_id
