from abc import ABC, abstractmethod
from typing import List, Optional

from .dto import TableInfo, JoinResult, LeaveResult


class ITableService(ABC):
    """Application service for table management."""

    @abstractmethod
    async def list_tables(self) -> List[TableInfo]:
        """Get all available tables with current state."""

    @abstractmethod
    async def join_table(self, player_id: str, table_id: str, buy_in: int) -> JoinResult:
        """Join a table with specified buy-in."""

    @abstractmethod
    async def leave_table(self, player_id: str, table_id: str) -> LeaveResult:
        """Leave table and trigger settlement."""


class ITableRegistry(ABC):
    """Registry for locating tables across servers."""

    @abstractmethod
    async def get_server_for_table(self, table_id: str) -> Optional[str]:
        """Returns game server URL hosting this table."""

    @abstractmethod
    async def assign_table_to_server(self, table_id: str) -> str:
        """Assigns table to least loaded server and returns URL."""
