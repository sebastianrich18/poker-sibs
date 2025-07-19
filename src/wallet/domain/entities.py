from typing import List
from DateTime import DateTime
from player.domain.entities import PlayerId
from table.domain.entities import TableId
from wallet.domain.value_objects import Reservation, Transaction





class WalletId:
    pass


class Wallet:
    id: WalletId
    owner_id: PlayerId
    available_balance: float
    reservations: List[Reservation]
    transactions: List[Transaction]

    def reserve_funds(self, amount: float) -> Reservation:
        pass

    def release_reservation(self, reservation: Reservation) -> bool:
        pass

    def apply_transaction(self, transaction: Transaction) -> bool:
        pass
