from fastapi import FastAPI, HTTPException
import asyncpg
import os

from ..domain.entities import (
    LoginRequest,
    CreateAccountRequest,
    LobbyJoinRequest,
    LeaveRequest,
)
from ...core.infrastructure import PostgresUserRepository, PostgresLobbyRepository
from ...core.domain.entities import Lobby, User, EntityId

app = FastAPI(title="Coordinator")

pool: asyncpg.pool.Pool | None = None
user_repo: PostgresUserRepository | None = None
lobby_repo: PostgresLobbyRepository | None = None


@app.on_event("startup")
async def startup() -> None:
    global pool, user_repo, lobby_repo
    database_url = os.getenv("DATABASE_URL", "postgresql://user:pass@localhost/postgres")
    pool = await asyncpg.create_pool(database_url)
    user_repo = PostgresUserRepository(pool)
    lobby_repo = PostgresLobbyRepository(pool)
    lobbies = await lobby_repo.list()
    if not lobbies:
        await pool.execute(
            "INSERT INTO lobbies (id, name, max_players, status) VALUES ('1', 'Main Lobby', 5, 'waiting')"
        )


@app.on_event("shutdown")
async def shutdown() -> None:
    if pool:
        await pool.close()


@app.post("/create-account")
async def create_account(req: CreateAccountRequest):
    assert user_repo
    existing = await user_repo.get_by_username(req.username)
    if existing:
        raise HTTPException(status_code=400, detail="User exists")
    user = await user_repo.create(req.username, req.password)
    return user


@app.post("/login")
async def login(req: LoginRequest):
    assert user_repo
    user = await user_repo.get_by_username(req.username)
    if not user or user.hashed_password != req.password:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    return user


@app.get("/user/{user_id}")
async def get_user(user_id: str):
    assert user_repo
    user = await user_repo.get_by_id(EntityId(user_id))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.get("/lobby")
async def list_lobbies():
    assert lobby_repo
    return await lobby_repo.list()


@app.get("/lobby/{lobby_id}")
async def get_lobby(lobby_id: str):
    assert lobby_repo
    lobby = await lobby_repo.get_by_id(EntityId(lobby_id))
    if not lobby:
        raise HTTPException(status_code=404, detail="Lobby not found")
    return lobby


@app.post("/lobby/{lobby_id}/join")
async def join_lobby(lobby_id: str, req: LobbyJoinRequest):
    assert lobby_repo and user_repo
    lobby = await lobby_repo.get_by_id(EntityId(lobby_id))
    user = await user_repo.get_by_id(req.user_id)
    if not lobby or not user:
        raise HTTPException(status_code=404, detail="Not found")
    if user.in_lobby:
        raise HTTPException(status_code=400, detail="Already in lobby")
    if len(lobby.players) >= lobby.max_players:
        raise HTTPException(status_code=400, detail="Lobby full")
    lobby.players.append(user.id)
    user.in_lobby = True
    await lobby_repo.update(lobby)
    await user_repo.update(user)
    return {"chips": user.chips}


@app.post("/lobby/{lobby_id}/user/{user_id}/leave")
async def leave_lobby(lobby_id: str, user_id: str, req: LeaveRequest):
    assert lobby_repo and user_repo
    lobby = await lobby_repo.get_by_id(EntityId(lobby_id))
    user = await user_repo.get_by_id(EntityId(user_id))
    if not lobby or not user:
        raise HTTPException(status_code=404, detail="Not found")
    if user_id in [str(u) for u in lobby.players]:
        lobby.players.remove(EntityId(user_id))
    user.chips = req.chips
    user.in_lobby = False
    await lobby_repo.update(lobby)
    await user_repo.update(user)
    return {"status": "ok"}
