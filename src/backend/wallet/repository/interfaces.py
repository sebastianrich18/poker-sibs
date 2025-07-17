from abc import ABC, abstractmethod
from typing import Optional

from ..domain.models import Player, PlayerWallet


class IPlayerRepository(ABC):
    @abstractmethod
    async def get_by_id(self, player_id: str) -> Optional[Player]:
        pass

    @abstractmethod
    async def get_by_username(self, username: str) -> Optional[Player]:
        pass

    @abstractmethod
    async def create(self, player: Player) -> None:
        pass

    @abstractmethod
    async def update(self, player: Player) -> None:
        pass


class IWalletRepository(ABC):
    @abstractmethod
    async def get_wallet(self, player_id: str) -> PlayerWallet:
        pass

    @abstractmethod
    async def save_wallet(self, wallet: PlayerWallet) -> None:
        pass
