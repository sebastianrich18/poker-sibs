# Poker Platform Design Document

## 1. Overview

This document outlines the design for an online poker platform using Domain-Driven Design (DDD) principles. The system is designed to start as a monolithic application with clear boundaries that allow evolution into a distributed system.

### Key Design Decisions
- **Synchronous-first architecture** with interfaces that support future event-driven migration
- **In-memory game state** with persistence only for completed hands and financial transactions
- **Three bounded contexts**: Table Management, Wallet, and Game
- **WebSocket for real-time gameplay**, REST for other operations

## 2. Architecture Principles

### Domain-Driven Design
- Clear bounded contexts with defined responsibilities
- Rich domain models encapsulating business logic
- Application services for orchestration
- Infrastructure adapters for external concerns

### Layered Architecture
```
Domain Layer:       Pure business logic, no external dependencies
Application Layer:  Use case orchestration, service interfaces
Infrastructure:     External integrations, persistence, APIs
```

### Interface-Driven Design
All inter-context communication through interfaces, enabling:
- Easy testing with mocks
- Swappable implementations (sync → async)
- Clear contracts between contexts

## 3. Context Map

```
┌─────────────────────────────────────────────────────┐
│                   POKER PLATFORM                     │
├─────────────────────────────────────────────────────┤
│                                                      │
│  ┌────────────────┐      ┌────────────────┐        │
│  │ Table Context  │      │ Wallet Context │        │
│  │   (Config &    │      │   (Money &     │        │
│  │  Orchestration)│ ───> │  Reservations) │        │
│  └───────┬────────┘      └────────────────┘        │
│          │                         ↑                 │
│          ↓                         │                 │
│  ┌────────────────────────────────┴────┐            │
│  │         Game Context                 │            │
│  │    (Poker Rules & Live State)       │            │
│  └──────────────────────────────────────┘            │
└──────────────────────────────────────────────────────┘
```

## 4. Context Details

### 4.1 Table Context

**Purpose**: Manage table configurations and orchestrate player seating

#### Domain Models
```python
class TableConfig:
    id: str
    name: str
    stakes: str  # "1/2", "5/10"
    max_seats: int
    min_buy_in: int
    max_buy_in: int
```

#### Application Interfaces
```python
class ITableService(ABC):
    @abstractmethod
    async def list_tables(self) -> List[TableInfo]:
        """Get all available tables with current state"""
        
    @abstractmethod
    async def join_table(self, player_id: str, table_id: str, buy_in: int) -> JoinResult:
        """Join a table with specified buy-in"""
        
    @abstractmethod
    async def leave_table(self, player_id: str, table_id: str) -> LeaveResult:
        """Leave table and trigger settlement"""

class ITableRegistry(ABC):
    """For distributed deployment - tracks table locations"""
    
    @abstractmethod
    async def get_server_for_table(self, table_id: str) -> Optional[str]:
        """Returns game server URL hosting this table"""
        
    @abstractmethod
    async def assign_table_to_server(self, table_id: str) -> str:
        """Assigns table to least loaded server"""
```

#### Data Transfer Objects
```python
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
    error_reason: Optional[str]
```

### 4.2 Wallet Context

**Purpose**: Manage player account balances and table reservations

#### Domain Models
```python
class PlayerWallet:
    player_id: str
    account_balance: int
    reservations: Dict[str, Reservation]
    
    def available_balance(self) -> int:
        """Balance minus active reservations"""
    
    def can_afford(self, amount: int) -> bool:
        """Check if player can afford amount"""
    
    def create_reservation(self, table_id: str, amount: int) -> Reservation:
        """Reserve chips for table"""
    
    def settle_reservation(self, table_id: str, final_stack: int) -> int:
        """Calculate and apply stack delta"""

class Reservation:
    id: str
    player_id: str
    table_id: str
    amount: int
    created_at: datetime
    status: ReservationStatus  # ACTIVE, SETTLED
```

#### Application Interfaces
```python
class IWalletService(ABC):
    @abstractmethod
    async def get_balance(self, player_id: str) -> BalanceInfo:
        """Get total and available balance"""
        
    @abstractmethod
    async def reserve_chips(self, player_id: str, table_id: str, amount: int) -> ReservationResult:
        """Reserve chips for table buy-in"""
        
    @abstractmethod
    async def settle_table(self, player_id: str, table_id: str, final_stack: int) -> SettlementResult:
        """Settle reservation with final chip count"""
        
    @abstractmethod
    async def get_reservations(self, player_id: str) -> List[Reservation]:
        """Get all active reservations"""
```

#### Repository Interface
```python
class IWalletRepository(ABC):
    @abstractmethod
    async def get_wallet(self, player_id: str) -> PlayerWallet:
        pass
        
    @abstractmethod
    async def save_wallet(self, wallet: PlayerWallet) -> None:
        pass
```

### 4.3 Game Context

**Purpose**: Execute poker game logic and maintain live game state

#### Domain Models
```python
class PokerGame:
    table_id: str
    seats: Dict[int, str]  # seat_num -> player_id
    stacks: Dict[str, int]  # player_id -> chips
    current_hand: Optional[HandState]
    dealer_button: int
    
    def add_player(self, player_id: str, seat: int, chips: int) -> None:
        """Add player to game"""
    
    def remove_player(self, player_id: str) -> int:
        """Remove player and return final stack"""
    
    def can_start_hand(self) -> bool:
        """Check if enough players to start"""
    
    def start_new_hand(self, shuffle_seed: str) -> HandState:
        """Initialize new hand"""

class HandState:
    hand_id: str
    players: List[str]
    player_cards: Dict[str, List[Card]]
    community_cards: List[Card]
    pot: int
    current_round: BettingRound  # PREFLOP, FLOP, TURN, RIVER
    action_on: str  # player_id
    last_aggressor: Optional[str]
    betting_history: List[PlayerAction]
    
    def apply_action(self, player_id: str, action: Action) -> ActionResult:
        """Apply and validate player action"""
    
    def is_complete(self) -> bool:
        """Check if hand is complete"""
```

#### Domain Services
```python
class PokerRulesEngine:
    @staticmethod
    def validate_action(state: HandState, player_id: str, action: Action) -> bool:
        """Validate if action is legal"""
    
    @staticmethod
    def determine_winners(state: HandState) -> List[str]:
        """Determine winner(s) of hand"""
    
    @staticmethod
    def calculate_payouts(pot: int, winners: List[str]) -> Dict[str, int]:
        """Calculate pot distribution"""

class DeckService:
    def __init__(self, randomness: IRandomnessProvider):
        pass
    
    async def create_shuffled_deck(self, seed: str) -> List[Card]:
        """Create deterministically shuffled deck"""
```

#### Domain Interfaces
```python
class IRandomnessProvider(ABC):
    @abstractmethod
    async def generate_seed(self) -> str:
        """Generate cryptographic seed"""
        
    @abstractmethod
    async def shuffle(self, items: List[any], seed: str) -> List[any]:
        """Deterministic shuffle with seed"""
```

#### Application Interfaces
```python
class IGameService(ABC):
    @abstractmethod
    async def start_round_if_ready(self, table_id: str) -> Optional[str]:
        """Start new hand if conditions met"""
        
    @abstractmethod
    async def process_player_action(self, table_id: str, player_id: str, action: dict) -> ActionResult:
        """Process game action"""
        
    @abstractmethod
    async def get_current_state(self, table_id: str, player_id: str) -> GameState:
        """Get game state from player perspective"""
        
    @abstractmethod
    async def add_player(self, table_id: str, player_id: str, buy_in: int) -> None:
        """Add player to game"""
        
    @abstractmethod
    async def remove_player(self, table_id: str, player_id: str) -> int:
        """Remove player and return final stack"""

class IHandHistoryRepository(ABC):
    @abstractmethod
    async def save_completed_hand(self, hand: CompletedHand) -> None:
        """Persist completed hand for audit"""
```

#### Data Transfer Objects
```python
@dataclass
class GameState:
    """Complete game state for UI rendering"""
    table_id: str
    seats: Dict[int, Optional[PlayerInfo]]
    community_cards: List[str]
    pot: int
    current_round: str
    action_on: Optional[str]
    available_actions: List[AvailableAction]
    my_cards: Optional[List[str]]  # Only for requesting player
    
@dataclass
class ActionResult:
    success: bool
    error_reason: Optional[str]
    new_state: Optional[GameState]
    
@dataclass
class CompletedHand:
    """Persisted after hand completion"""
    hand_id: str
    table_id: str
    players: List[PlayerHandInfo]
    all_actions: List[str]  # Compressed action log
    community_cards: List[str]
    winners: List[str]
    pot_distribution: Dict[str, int]
    rake: int
    shuffle_seed: str
    completed_at: datetime
```

## 5. API Design

### 5.1 REST Endpoints

```
GET  /api/tables                    # List available tables
POST /api/tables/{id}/join          # Join table (returns WebSocket URL)
POST /api/tables/{id}/leave         # Leave table

GET  /api/wallet/balance            # Get player balance
GET  /api/wallet/reservations       # Get active reservations
```

### 5.2 WebSocket Interface

```
WS /ws/tables/{table_id}            # Real-time game connection

# Client -> Server Messages
{
    "type": "action",
    "action": {
        "type": "bet|call|fold|check|raise",
        "amount": 100  // For bet/raise
    }
}

# Server -> Client Messages
{
    "type": "game_state",
    "data": GameState
}

{
    "type": "game_update",
    "data": {
        "event": "player_joined|player_left|hand_started|action_processed",
        "state": GameState
    }
}
```

## 6. Deployment Architecture

### 6.1 V1: Single Server

```
Client → REST API → TableService → GameService (in-memory)
         ↓                           ↓
         WebSocket ←─────────────────┘
```

**Characteristics:**
- All contexts in single process
- In-memory game state
- PostgreSQL for wallet and hand history
- Direct service calls between contexts

### 6.2 V2: Distributed System

```
                    ┌→ GameServer1 (tables 1-100)
Client → API Gateway├→ GameServer2 (tables 101-200)
         ↓          └→ GameServer3 (tables 201-300)
         │
         └→ Redis (table registry + shared state)
```

**Characteristics:**
- Table service acts as orchestrator
- Game servers handle specific table ranges
- Redis for table registry and cross-server state
- Event bus for inter-service communication

## 7. Data Persistence Strategy

### 7.1 What's Persisted

| Data Type | Storage | Reason |
|-----------|---------|---------|
| Wallet/Reservations | PostgreSQL | Financial data must be durable |
| Completed Hands | PostgreSQL | Audit trail, hand history |
| Table Config | In-memory/Config | Rarely changes |
| Live Game State | In-memory | Transient, high-frequency updates |

### 7.2 Database Schema (Simplified)

```sql
-- Wallet Context
CREATE TABLE wallets (
    player_id VARCHAR PRIMARY KEY,
    account_balance INTEGER NOT NULL,
    updated_at TIMESTAMP
);

CREATE TABLE reservations (
    id UUID PRIMARY KEY,
    player_id VARCHAR NOT NULL,
    table_id VARCHAR NOT NULL,
    amount INTEGER NOT NULL,
    status VARCHAR NOT NULL,
    created_at TIMESTAMP
);

-- Game Context (Audit Only)
CREATE TABLE completed_hands (
    hand_id UUID PRIMARY KEY,
    table_id VARCHAR NOT NULL,
    players JSONB NOT NULL,
    actions JSONB NOT NULL,
    winners JSONB NOT NULL,
    pot_distribution JSONB NOT NULL,
    completed_at TIMESTAMP
);
```

## 8. Cross-Cutting Concerns

### 8.1 Authentication
- JWT tokens for player authentication
- Token validation at API gateway
- Player ID extracted from token for all operations

### 8.2 Audit Logging
- All financial transactions logged
- Complete hand history stored
- Player actions recorded for dispute resolution

### 8.3 Error Handling
- Domain exceptions for business rule violations
- Infrastructure exceptions for technical failures
- Graceful degradation for non-critical operations

## 9. Future Considerations (V2)

### 9.1 Event-Driven Migration
- Replace direct service calls with event bus
- Implement saga pattern for distributed transactions
- Add event sourcing for game state

### 9.2 Scalability Enhancements
- Horizontal scaling of game servers
- Read replicas for wallet queries
- Caching layer for frequently accessed data

### 9.3 Additional Features
- Tournament support (different payout structure)
- Multiple game types (Omaha, Stud)
- Statistics and analytics context
- Social features (chat, friends)

## 10. Development Approach

### Phase 1: Core Functionality (Weekend Project)
1. Implement domain models
2. Create synchronous services
3. Basic REST API
4. Simple WebSocket game updates

### Phase 2: Production Readiness
1. Add comprehensive error handling
2. Implement audit logging
3. Performance optimization
4. Security hardening

### Phase 3: Scale Out
1. Implement table registry
2. Add distributed game servers
3. Migrate to event-driven architecture
4. Add monitoring and observability

