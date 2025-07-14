from typing import Protocol, Optional, List
from .entities import User, Lobby, EntityId


class UserRepository(Protocol):
    async def get_by_id(self, user_id: EntityId) -> Optional[User]:
        """Retrieve a user by ID."""

    async def get_by_username(self, username: str) -> Optional[User]:
        """Retrieve a user by their username."""

    async def create(self, username: str, password: str) -> User:
        """Create a new user entry."""

    async def update(self, user: User) -> None:
        """Persist updates to a user."""


class LobbyRepository(Protocol):
    async def list(self) -> List[Lobby]:
        ...

    async def get_by_id(self, lobby_id: EntityId) -> Optional[Lobby]:
        ...

    async def update(self, lobby: Lobby) -> None:
        ...
