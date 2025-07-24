from abc import ABC, abstractmethod

from shared.types import WalletId
from wallet.domain.entities import Wallet


class IWalletService(ABC):

    @abstractmethod
    async def get_balance(self, wallet_id: WalletId) -> Wallet:
        pass

    @abstractmethod
    async def get_active_reservations(self, wallet: Wallet) -> str:
        pass

    @abstractmethod
    async def create_reservation(self, wallet: Wallet) -> None:
        pass

    @abstractmethod
    async def apply_transaction(self, wallet: Wallet) -> None:
        pass


class IWalletQueryService(ABC):
    @abstractmethod
    async def get_wallet_balance(self, wallet_id: WalletId) -> float:
        pass

    @abstractmethod
    async def get_wallet_reservations(self, wallet_id: WalletId) -> list:
        pass

    @abstractmethod
    async def get_wallet_transactions(self, wallet_id: WalletId) -> list:
        pass
