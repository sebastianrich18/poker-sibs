**Bounded Contexts and Their Roles: Poker Sibs (DDD)**

---

### 1. Gameplay Context

**Responsibility**: Managing game state, rules, and resolution.

* **Game Engine**: Pure domain logic—validates actions, updates hand state, calculates winners
* **Game Session**: Real-time orchestration—manages WebSocket connections, turn timers, and heartbeats.
* **Game Ledger**: Manages a leadger for every hand, is included in LeaveEvent for settlement
* Consumes: `JoinRequestEvent`, `LeaveRequestEvent`, `TableStartRequestEvent`, `TableStopRequestEvent`
* Supplies: `JoinEvent`, `LeaveEvent`, `TableStartEvent`, `TableStopEvent`, `HandCompletedEvent`

---

### 2. Lobby & Table Management Context

**Responsibility**: Player flow and table lifecycle management.

* Manages tables, seating, and player queues.
* Coordinates table creation/destruction.
* Validates player eligibility based on buy-in.
* Consumes: `TableStartEvent`, `TableStopEvent`
* Supplies: `TableStartRequestEvent`, `TableStopRequestEvent`, `JoinRequestEvent`, `LeaveRequestEvent`

---

### 3. Settlement Context

**Responsibility**: Authoritative ledger for chip ownership and transfer.

* Manages chip reservations and balances.
* Applies chip deltas and resolves reservations.
* Critical for audit and correctness.
* Implements compensating logic for failure handling (e.g., expired reservations).
* Consumes: `JoinEvent`, `LeaveEvent`
* Supplies: `ReservationCreatedEvent`, `SettlementAppliedEvent` (just for auditability, not consumed currently)


### Future Contexts
1. Audit: Validate ledger, settlements, and reservations
2. Analytics: Replay all played hands
