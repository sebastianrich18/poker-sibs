from abc import ABC
from wallet.domain.entities import Wallet, WalletId


class WalletRepository(ABC):
    async def get_by_id(self, wallet_id: WalletId) -> float:
        pass

    async def create(self, wallet: Wallet) -> str:
        pass

    async def update(self, wallet: Wallet) -> None:
        pass
