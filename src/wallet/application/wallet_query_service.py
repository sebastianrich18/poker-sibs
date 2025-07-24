from wallet.application.interfaces import IWalletQueryService, IWalletService


class FileSystemWalletQueryService(IWalletService):
    """
    Implementation of WalletQueryService for file system storage.
    """

    async def get_wallet_balance(self, wallet_id: str) -> float:
        # Placeholder for actual file system query logic
        return 100.0  # Example balance

    async def get_wallet_reservations(self, wallet_id: str) -> list:
        # Placeholder for actual file system query logic
        return []

    async def get_wallet_transactions(self, wallet_id: str) -> list:
        # Placeholder for actual file system query logic
        return []


class PostgresWalletQueryService(IWalletQueryService):
    """
    Implementation of WalletQueryService for PostgreSQL.
    """

    def __init__(self, db_session):
        self.db_session = db_session

    async def get_wallet_balance(self, wallet_id: str) -> float:
        # Placeholder for actual database query logic
        return 100.0  # Example balance

    async def get_wallet_reservations(self, wallet_id: str) -> list:
        # Placeholder for actual database query logic
        return []

    async def get_wallet_transactions(self, wallet_id: str) -> list:
        # Placeholder for actual database query logic
        return []
