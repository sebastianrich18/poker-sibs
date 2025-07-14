import os
from typing import Optional, List

import asyncpg

from ..domain.entities import User, Lobby, EntityId
from ..domain.interfaces import UserRepository, LobbyRepository


class PostgresUserRepository(UserRepository):
    def __init__(self, pool: asyncpg.pool.Pool) -> None:
        self.pool = pool

    async def get_by_id(self, user_id: EntityId) -> Optional[User]:
        row = await self.pool.fetchrow(
            "SELECT id, username, hashed_password, chips, in_lobby FROM users WHERE id=$1",
            str(user_id),
        )
        return User(**row) if row else None

    async def get_by_username(self, username: str) -> Optional[User]:
        row = await self.pool.fetchrow(
            "SELECT id, username, hashed_password, chips, in_lobby FROM users WHERE username=$1",
            username,
        )
        return User(**row) if row else None

    async def create(self, username: str, password: str) -> User:
        row = await self.pool.fetchrow(
            "INSERT INTO users (username, hashed_password, chips, in_lobby) "
            "VALUES ($1, $2, 1000, false) "
            "RETURNING id, username, hashed_password, chips, in_lobby",
            username,
            password,
        )
        return User(**row)

    async def update(self, user: User) -> None:
        await self.pool.execute(
            "UPDATE users SET username=$1, hashed_password=$2, chips=$3, in_lobby=$4 WHERE id=$5",
            user.username,
            user.hashed_password,
            user.chips,
            user.in_lobby,
            str(user.id),
        )


class PostgresLobbyRepository(LobbyRepository):
    def __init__(self, pool: asyncpg.pool.Pool) -> None:
        self.pool = pool

    def _row_to_lobby(self, row: asyncpg.Record) -> Lobby:
        players = row.get("players") or []
        if not isinstance(players, list):
            players = list(players)
        return Lobby(
            id=EntityId(str(row["id"])),
            name=row["name"],
            max_players=row["max_players"],
            players=[EntityId(str(p)) for p in players],
            status=row["status"],
        )

    async def list(self) -> List[Lobby]:
        rows = await self.pool.fetch(
            """
            SELECT l.id, l.name, l.max_players, l.status,
                   COALESCE(array_agg(lp.user_id) FILTER (WHERE lp.user_id IS NOT NULL), '{}') AS players
            FROM lobbies l
            LEFT JOIN lobby_players lp ON l.id = lp.lobby_id
            GROUP BY l.id
            """
        )
        return [self._row_to_lobby(r) for r in rows]

    async def get_by_id(self, lobby_id: EntityId) -> Optional[Lobby]:
        row = await self.pool.fetchrow(
            """
            SELECT l.id, l.name, l.max_players, l.status,
                   COALESCE(array_agg(lp.user_id) FILTER (WHERE lp.user_id IS NOT NULL), '{}') AS players
            FROM lobbies l
            LEFT JOIN lobby_players lp ON l.id = lp.lobby_id
            WHERE l.id=$1
            GROUP BY l.id
            """,
            str(lobby_id),
        )
        return self._row_to_lobby(row) if row else None

    async def update(self, lobby: Lobby) -> None:
        await self.pool.execute(
            "UPDATE lobbies SET name=$1, max_players=$2, status=$3 WHERE id=$4",
            lobby.name,
            lobby.max_players,
            lobby.status,
            str(lobby.id),
        )
        await self.pool.execute(
            "DELETE FROM lobby_players WHERE lobby_id=$1",
            str(lobby.id),
        )
        if lobby.players:
            await self.pool.executemany(
                "INSERT INTO lobby_players (lobby_id, user_id) VALUES ($1, $2)",
                [(str(lobby.id), str(uid)) for uid in lobby.players],
            )
