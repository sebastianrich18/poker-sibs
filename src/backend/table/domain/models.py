from dataclasses import dataclass

@dataclass
class TableConfig:
    """Configuration for a poker table."""
    id: str
    name: str
    stakes: str  # e.g. "1/2", "5/10"
    max_seats: int
    min_buy_in: int
    max_buy_in: int
