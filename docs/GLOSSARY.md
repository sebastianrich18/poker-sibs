**Glossary: Poker Sibs (DDD)**

---

### Core Domain Terms

* **Player**: A user participating in a game. Authenticated via JWT. Has preferences and an account identity.
* **Chips**: The quantifiable unit used for betting and settlements within a game. Represents value but may or may not map directly to currency.
* **Stack**: The number of chips a player has *at a table*.
* **Account Balance**: The total number of chips a player owns platform-wide, managed by the Settlement context.
* **Buy-in**: The required amount of chips to join a table.

---

### Gameplay Terms

* **Hand**: A full cycle of play from dealing hole cards to resolving the pot.
* **Round**: A single betting phase within a hand. There are four: Pre-Flop, Flop, Turn, River.
* **Hole Cards**: The two private cards dealt to each player.
* **Community Cards**: Up to five shared cards placed face-up on the table.
* **Flop**: The first three community cards.
* **Turn**: The fourth community card.
* **River**: The fifth and final community card.
* **Pot**: The total chips wagered by players in a hand.
* **Side Pot**: A secondary pot created when players go all-in with different chip amounts.
* **Dealer Button**: Marker indicating dealer position; determines betting order.
* **Showdown**: The final stage of a hand where remaining players reveal cards.
* **Big Blind (BB)**: A forced bet made by the player two seats left of the Dealer Button before any cards are dealt.
* **Small Blind (SB)**: A smaller forced bet made by the player immediately left of the Dealer Button.

---

### Player Actions

* **Wager**: Any action involving placing chips into the pot—includes betting, raising, calling, and all-ins.
* **Bet**: The first wager made during a round.
* **Raise**: Increasing the current highest bet.
* **Call**: Matching the current highest bet.
* **Check**: Passing the action to the next player without betting.
* **Fold**: Exiting the hand by forfeiting any claim to the pot.
* **All-In**: Betting all remaining chips.
* **Muck**: Choosing not to reveal cards at the showdown.

---

### System Constructs

* **Lobby**: Interface where players can browse and queue for tables.
* **Room**: A container instance capable of managing multiple tables.
* **Table**: The execution environment for a single game.
* **Seat**: A position at the table that can be occupied by a player.
* **Action**: A player's opportunity to make a move during their turn.
* **Stack Delta**: The net change in a player's chip stack at the conclusion of a hand. Can be positive or negative.
* **Reservation**: A temporary hold on a player’s chips before seating or settlement.

---

### Infrastructure and Platform

* **JWT**: JSON Web Token used for authentication and session validation.
* **Event**: An immutable fact emitted by a context (e.g., GameEnded, PlayerSeated).
* **Command**: A request to perform an action (e.g., ReserveChips, JoinTable).
* **Saga**: A long-running transaction mechanism for orchestrating cross-context operations.
* **SettlementEntry**: A ledger record reflecting a stack delta.
* **Rake**: A small fee collected per hand (optional).
* **Sit Out**: A temporary non-participation status at a table.
* **Seat Open**: Triggered when a seat becomes available for waiting players.
