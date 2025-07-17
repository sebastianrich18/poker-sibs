from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Dict, Optional


class ReservationStatus(str, Enum):
    ACTIVE = "ACTIVE"
    SETTLED = "SETTLED"


@dataclass
class Player:
    id: str
    username: str
    password_hash: str
    created_at: datetime
    last_login: Optional[datetime] = None

    def verify_password(self, password: str) -> bool:
        # Placeholder for password verification logic
        import bcrypt
        return bcrypt.checkpw(password.encode(), self.password_hash.encode())

    def update_password(self, new_password: str) -> None:
        import bcrypt
        self.password_hash = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt()).decode()


@dataclass
class Reservation:
    id: str
    player_id: str
    table_id: str
    amount: int
    created_at: datetime
    status: ReservationStatus = ReservationStatus.ACTIVE


@dataclass
class PlayerWallet:
    player_id: str
    account_balance: int
    reservations: Dict[str, Reservation] = field(default_factory=dict)

    def available_balance(self) -> int:
        reserved = sum(r.amount for r in self.reservations.values() if r.status == ReservationStatus.ACTIVE)
        return self.account_balance - reserved

    def can_afford(self, amount: int) -> bool:
        return self.available_balance() >= amount

    def create_reservation(self, table_id: str, amount: int) -> Reservation:
        if not self.can_afford(amount):
            raise ValueError("Insufficient funds")
        res_id = f"res-{len(self.reservations)+1}"
        reservation = Reservation(
            id=res_id,
            player_id=self.player_id,
            table_id=table_id,
            amount=amount,
            created_at=datetime.utcnow(),
        )
        self.reservations[table_id] = reservation
        return reservation

    def settle_reservation(self, table_id: str, final_stack: int) -> int:
        reservation = self.reservations.get(table_id)
        if not reservation or reservation.status != ReservationStatus.ACTIVE:
            raise ValueError("No active reservation")
        delta = final_stack - reservation.amount
        reservation.status = ReservationStatus.SETTLED
        self.account_balance += delta
        return delta
