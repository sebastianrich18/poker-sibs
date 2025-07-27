from fastapi import APIRouter, HTTPException

from api.schemas import (
    CreatePlayerResponse,
    GetPlayerResponse,
    CreatePlayerRequest,
    LoginPlayerRequest,
    LoginPlayerResponse,
)
from player.application.player_query_service import FileSystemPlayerQueryService
from player.application.player_service import PlayerService


player_router = APIRouter(prefix="/v1/player", tags=["Player"])


@player_router.get("/{player_id}", response_model=GetPlayerResponse)
async def get_player(player_id: int):
    """
    Retrieve player information by player ID.
    """
    player_query_service = FileSystemPlayerQueryService()
    try:
        player = player_query_service.get_player(player_id)
        return GetPlayerResponse(**player)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@player_router.post("/login", response_model=LoginPlayerResponse)
async def player_login(login_request: LoginPlayerRequest):
    """
    Log in a player by player ID.
    """
    player_service = PlayerService()
    try:
        player = player_service.login(
            username=login_request.username, password=login_request.password
        )
        if not player:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        return LoginPlayerResponse(
            access_token="some_access_token", token_type="bearer"
        )
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))


@player_router.post("/register", response_model=CreatePlayerResponse)
async def create_player(player: CreatePlayerRequest):
    """
    Create a new player.
    """
    player_service = PlayerService()
    try:
        player_service.register(
            username=player.username, password=player.password
        )
        return CreatePlayerResponse(
            access_token="some_access_token", token_type="bearer"
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
