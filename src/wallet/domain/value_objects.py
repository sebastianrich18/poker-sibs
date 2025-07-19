from datetime import datetime

from player.domain.entities import PlayerId
from table.domain.entities import TableId


class ReservationId:
    pass


class TransactionId:
    pass

class Reservation:
    id: ReservationId
    table_id: TableId
    player_id: PlayerId
    amount: float
    is_active: bool
    timestamp: datetime


class Transaction:
    id: TransactionId
    wallet_id: str
    amount: float
    reason: str
    timestamp: datetime
