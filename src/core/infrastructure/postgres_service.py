import os
from typing import Optional, List

import asyncpg

from ..domain.entities import User, Lobby
from ..domain.interfaces import UserRepository, LobbyRepository


class PostgresService:
    """Lightweight wrapper around an asyncpg connection pool."""

    def __init__(self, dsn: str | None = None) -> None:
        self.dsn = dsn or os.getenv("DATABASE_URL", "postgresql://user:pass@localhost/postgres")
        self.pool: asyncpg.pool.Pool | None = None

    async def __aenter__(self) -> "PostgresService":
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        await self.disconnect()

    async def connect(self) -> None:
        self.pool = await asyncpg.create_pool(self.dsn)

    async def disconnect(self) -> None:
        if self.pool:
            await self.pool.close()
            self.pool = None


class PostgresUserRepository(UserRepository):
    def __init__(self, service: PostgresService):
        self.service = service

    async def get(self, user_id: str) -> Optional[User]:
        row = await self.service.pool.fetchrow(
            "SELECT id, username, hashed_password, chips, in_lobby FROM users WHERE id=$1",
            user_id,
        )
        return User(**row) if row else None

    async def get_by_username(self, username: str) -> Optional[User]:
        row = await self.service.pool.fetchrow(
            "SELECT id, username, hashed_password, chips, in_lobby FROM users WHERE username=$1",
            username,
        )
        return User(**row) if row else None

    async def create(self, username: str, password: str) -> User:
        row = await self.service.pool.fetchrow(
            "INSERT INTO users (username, hashed_password, chips, in_lobby) "
            "VALUES ($1, $2, 1000, false) "
            "RETURNING id, username, hashed_password, chips, in_lobby",
            username,
            password,
        )
        return User(**row)

    async def update(self, user: User) -> None:
        await self.service.pool.execute(
            "UPDATE users SET username=$1, hashed_password=$2, chips=$3, in_lobby=$4 WHERE id=$5",
            user.username,
            user.hashed_password,
            user.chips,
            user.in_lobby,
            user.id,
        )


class PostgresLobbyRepository(LobbyRepository):
    def __init__(self, service: PostgresService):
        self.service = service

    def _row_to_lobby(self, row: asyncpg.Record) -> Lobby:
        players = row["players"] or []
        if not isinstance(players, list):
            players = list(players)
        return Lobby(
            id=str(row["id"]),
            name=row["name"],
            max_players=row["max_players"],
            players=players,
            status=row["status"],
        )

    async def list(self) -> List[Lobby]:
        rows = await self.service.pool.fetch(
            "SELECT id, name, max_players, players, status FROM lobbies"
        )
        return [self._row_to_lobby(r) for r in rows]

    async def get(self, lobby_id: str) -> Optional[Lobby]:
        row = await self.service.pool.fetchrow(
            "SELECT id, name, max_players, players, status FROM lobbies WHERE id=$1",
            lobby_id,
        )
        return self._row_to_lobby(row) if row else None

    async def update(self, lobby: Lobby) -> None:
        await self.service.pool.execute(
            "UPDATE lobbies SET name=$1, max_players=$2, players=$3, status=$4 WHERE id=$5",
            lobby.name,
            lobby.max_players,
            lobby.players,
            lobby.status,
            lobby.id,
        )
