from dataclasses import dataclass
from typing import Optional, List

from ..domain.models import Reservation


@dataclass
class RegisterResult:
    success: bool
    player_id: Optional[str]
    error_reason: Optional[str]


@dataclass
class LoginResult:
    success: bool
    token: Optional[str]
    player_id: Optional[str]
    error_reason: Optional[str]


@dataclass
class BalanceInfo:
    total_balance: int
    available_balance: int
    reserved_amount: int


@dataclass
class ReservationResult:
    success: bool
    reservation: Optional[Reservation]
    error_reason: Optional[str]


@dataclass
class SettlementResult:
    success: bool
    delta: int
    error_reason: Optional[str]
