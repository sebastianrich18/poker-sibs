from dataclasses import dataclass
from typing import Optional


@dataclass
class TableInfo:
    id: str
    name: str
    stakes: str
    current_players: int
    max_players: int
    min_buy_in: int
    max_buy_in: int


@dataclass
class JoinResult:
    success: bool
    table_id: str
    seat_number: Optional[int]
    game_server_url: str
    error_reason: Optional[str] = None


@dataclass
class LeaveResult:
    success: bool
    error_reason: Optional[str] = None
