from abc import ABC, abstractmethod
from typing import List, Optional

from .dto import RegisterResult, LoginResult, BalanceInfo, ReservationResult, SettlementResult
from ..domain.models import Reservation


class IAuthService(ABC):
    @abstractmethod
    async def register(self, username: str, password: str, initial_balance: int = 1000) -> RegisterResult:
        """Register new player with initial balance."""

    @abstractmethod
    async def login(self, username: str, password: str) -> LoginResult:
        """Authenticate and return JWT."""

    @abstractmethod
    async def validate_token(self, token: str) -> Optional[str]:
        """Validate JWT and return player_id."""


class IWalletService(ABC):
    @abstractmethod
    async def get_balance(self, player_id: str) -> BalanceInfo:
        """Get total and available balance."""

    @abstractmethod
    async def reserve_chips(self, player_id: str, table_id: str, amount: int) -> ReservationResult:
        """Reserve chips for table buy-in."""

    @abstractmethod
    async def settle_table(self, player_id: str, table_id: str, final_stack: int) -> SettlementResult:
        """Settle reservation with final chip count."""

    @abstractmethod
    async def get_reservations(self, player_id: str) -> List[Reservation]:
        """Get all active reservations."""
