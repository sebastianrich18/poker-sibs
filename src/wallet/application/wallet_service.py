from shared.types import WalletId
from wallet.application.interfaces import IWalletService
from wallet.domain.entities import Wallet
from wallet.domain.value_objects import Reservation, Transaction


class WalletService(IWalletService):
    """
    Implementation of IWalletService for managing wallet operations.
    """

    def __init__(self, wallet_repository):
        self.wallet_repository = wallet_repository

    async def get_balance(self, wallet_id: WalletId) -> Wallet:
        pass

    async def get_active_reservations(self, wallet: Wallet) -> str:
        pass

    async def create_reservation(self, wallet: Wallet) -> None:
        pass
