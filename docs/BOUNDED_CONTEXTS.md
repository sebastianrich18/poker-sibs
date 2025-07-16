**Bounded Contexts and Their Roles: Poker Sibs (DDD)**

---

### 1. Players Context

**Responsibility**: Identity and authentication management.

* Owns player profiles and preferences.
* Issues JWTs for session management.
* Stateless service; no chip, session, or game state.
* Exposes: `authenticate()`, `getProfile()`, `updatePreferences()`

---

### 2. Gameplay Context

**Responsibility**: Managing game state, rules, and resolution.

**Modules**:

* **Game Engine**: Pure domain logic—validates actions, updates hand state, calculates winners.

* **Game Session**: Real-time orchestration—manages WebSocket connections, turn timers, and heartbeats.

* Consumes: `startGame(tableConfig)`, `playerAction(input)`

* Emits: `HandEnded`, `InvalidMove`, `TimerExpired`

---

### 3. Lobby & Table Management Context

**Responsibility**: Player flow and table lifecycle management.

* Manages tables, seating, and player queues.
* Coordinates table creation/destruction.
* Validates player eligibility based on buy-in.
* Emits: `PlayerSeated`, `SeatOpen`, `TableReady`
* Consumes: `reserveChips()`, `getAvailableTables()`

---

### 4. Settlement Context

**Responsibility**: Authoritative ledger for chip ownership and transfer.

* Manages chip reservations and balances.
* Applies deltas emitted from Gameplay via event-driven model.
* Critical for audit and correctness.
* Exposes: `reserveChips(playerId, amount)`, `applyWinnings(handId)`, `getBalance(playerId)`
* Emits: `ReservationCreated`, `BalanceUpdated`, `SettlementFailed`
* Implements compensating logic for failure handling (e.g., expired reservations).
