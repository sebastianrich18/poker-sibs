from fastapi import FastAPI, Depends, HTTPException, WebSocket
from pydantic import BaseModel
from typing import Dict, Optional, List
from uuid import uuid4

from backend.common.auth import generate_token, validate_token
from backend.common.middleware import get_current_player
from backend.wallet.domain.models import Player, PlayerWallet, ReservationStatus, Reservation
from backend.table.domain.models import TableConfig

app = FastAPI(title="Poker Backend")

# In-memory stores
players_by_username: Dict[str, Player] = {}
players_by_id: Dict[str, Player] = {}
wallets: Dict[str, PlayerWallet] = {}

tables: Dict[str, TableConfig] = {
    "1": TableConfig(id="1", name="Low Stakes", stakes="1/2", max_seats=6, min_buy_in=100, max_buy_in=200),
    "2": TableConfig(id="2", name="Medium Stakes", stakes="5/10", max_seats=6, min_buy_in=500, max_buy_in=1000),
}
# seat assignments: table_id -> seat_num -> player_id
seats: Dict[str, Dict[int, Optional[str]]] = {tid: {i: None for i in range(1, cfg.max_seats+1)} for tid, cfg in tables.items()}


# Request models
class RegisterRequest(BaseModel):
    username: str
    password: str

class LoginRequest(BaseModel):
    username: str
    password: str

class JoinRequest(BaseModel):
    buy_in: int


@app.post("/api/auth/register")
async def register(req: RegisterRequest):
    if req.username in players_by_username:
        raise HTTPException(status_code=409, detail="Username taken")
    import bcrypt
    player_id = str(uuid4())
    password_hash = bcrypt.hashpw(req.password.encode(), bcrypt.gensalt()).decode()
    player = Player(id=player_id, username=req.username, password_hash=password_hash, created_at=__import__("datetime").datetime.utcnow())
    players_by_username[req.username] = player
    players_by_id[player_id] = player
    wallets[player_id] = PlayerWallet(player_id=player_id, account_balance=1000)
    return {"success": True, "player_id": player_id}


@app.post("/api/auth/login")
async def login(req: LoginRequest):
    player = players_by_username.get(req.username)
    if not player:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    import bcrypt
    if not bcrypt.checkpw(req.password.encode(), player.password_hash.encode()):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = generate_token(player.id, player.username)
    return {"success": True, "token": token, "player_id": player.id}


@app.get("/api/tables")
async def list_tables():
    info = []
    for cfg in tables.values():
        current_players = sum(1 for p in seats[cfg.id].values() if p)
        info.append({
            "id": cfg.id,
            "name": cfg.name,
            "stakes": cfg.stakes,
            "current_players": current_players,
            "max_players": cfg.max_seats,
            "min_buy_in": cfg.min_buy_in,
            "max_buy_in": cfg.max_buy_in,
        })
    return info


@app.post("/api/tables/{table_id}/join")
async def join_table(table_id: str, join: JoinRequest, player_id: str = Depends(get_current_player)):
    cfg = tables.get(table_id)
    if not cfg:
        raise HTTPException(status_code=404, detail="Table not found")
    wallet = wallets[player_id]
    if not wallet.can_afford(join.buy_in):
        raise HTTPException(status_code=403, detail="Insufficient funds")
    seat_map = seats[table_id]
    seat_num = next((s for s, p in seat_map.items() if p is None), None)
    if seat_num is None:
        raise HTTPException(status_code=409, detail="Table full")
    wallet.create_reservation(table_id, join.buy_in)
    seat_map[seat_num] = player_id
    wallet.account_balance -= join.buy_in
    return {"success": True, "table_id": table_id, "seat_number": seat_num, "game_server_url": "ws://localhost/ws/tables/" + table_id}


@app.post("/api/tables/{table_id}/leave")
async def leave_table(table_id: str, player_id: str = Depends(get_current_player)):
    cfg = tables.get(table_id)
    if not cfg:
        raise HTTPException(status_code=404, detail="Table not found")
    seat_map = seats[table_id]
    seat = next((s for s, p in seat_map.items() if p == player_id), None)
    if seat is None:
        raise HTTPException(status_code=404, detail="Player not at table")
    seat_map[seat] = None
    wallet = wallets[player_id]
    final_stack = wallet.reservations[table_id].amount  # simplification: assume no change
    delta = wallet.settle_reservation(table_id, final_stack)
    return {"success": True, "delta": delta}


@app.get("/api/wallet/balance")
async def get_balance(player_id: str = Depends(get_current_player)):
    wallet = wallets[player_id]
    total = wallet.account_balance
    reserved = sum(r.amount for r in wallet.reservations.values() if r.status == ReservationStatus.ACTIVE)
    available = wallet.available_balance()
    return {"total_balance": total, "available_balance": available, "reserved_amount": reserved}


@app.get("/api/wallet/reservations")
async def get_reservations(player_id: str = Depends(get_current_player)):
    wallet = wallets[player_id]
    return list(wallet.reservations.values())


@app.get("/api/player/profile")
async def profile(player_id: str = Depends(get_current_player)):
    player = players_by_id[player_id]
    return {"player_id": player.id, "username": player.username}


@app.websocket("/ws/tables/{table_id}")
async def table_ws(websocket: WebSocket, table_id: str, token: str):
    payload = validate_token(token)
    if not payload:
        await websocket.close(code=1008)
        return
    await websocket.accept()
    await websocket.send_json({"type": "game_state", "data": {"table_id": table_id}})
    try:
        while True:
            await websocket.receive_text()
            await websocket.send_json({"type": "game_update", "data": {"event": "noop"}})
    except Exception:
        await websocket.close()
