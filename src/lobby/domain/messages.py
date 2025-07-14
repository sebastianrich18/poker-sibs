# web socket messages exchanged between lobby and clients
from pydantic import BaseModel
from typing import Optional, Dict, Union, Literal, Tuple

from src.core.domain.entities import UserId
from src.lobby.domain.entities import BettingAction, Card, Rank, Suit

# Base message structure
class WebSocketMessage(BaseModel):
    type: str

# Server to Client Messages
class JoinAckMessage(WebSocketMessage):
    type: Literal["join-ack"] = "join-ack"
    userId: UserId
    seat: int

class ErrorMessage(WebSocketMessage):
    type: Literal["error"] = "error"
    error: str

class HeartbeatMessage(WebSocketMessage):
    type: Literal["heartbeat"] = "heartbeat"

class PlayerJoinedMessage(WebSocketMessage):
    type: Literal["player-joined"] = "player-joined"
    userId: UserId
    seat: int

class PlayerLeftMessage(WebSocketMessage):
    type: Literal["player-left"] = "player-left"
    userId: UserId

class HoleCardMessage(WebSocketMessage):
    type: Literal["hole-card"] = "hole-card"
    card: Card

class FlopMessage(WebSocketMessage):
    type: Literal["flop"] = "flop"
    cards: Tuple[Card, Card, Card]

class TurnMessage(WebSocketMessage):
    type: Literal["turn"] = "turn"
    card: Card

class RiverMessage(WebSocketMessage):
    type: Literal["river"] = "river"
    card: Card

class ActionBroadcastMessage(WebSocketMessage):
    type: Literal["action-broadcast"] = "action-broadcast"
    userId: UserId
    action: BettingAction
    amount: Optional[float] = None

class RoundResultMessage(WebSocketMessage):
    type: Literal["round-result"] = "round-result"
    results: Dict[UserId, int]  # userId -> chip delta

# Client to Server Messages
class ActionMessage(WebSocketMessage):
    type: Literal["action"] = "action"
    action: BettingAction
    amount: Optional[int] = None

class LeaveMessage(WebSocketMessage):
    type: Literal["leave"] = "leave"

# Union type for all possible messages
ClientMessage = Union[ActionMessage, LeaveMessage, HeartbeatMessage]
ServerMessage = Union[
    JoinAckMessage,
    ErrorMessage,
    PlayerJoinedMessage,
    PlayerLeftMessage,
    HoleCardMessage,
    FlopMessage,
    TurnMessage,
    RiverMessage,
    ActionBroadcastMessage,
    RoundResultMessage,
    ErrorMessage,
    JoinAckMessage,
]



