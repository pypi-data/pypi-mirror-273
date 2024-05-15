from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class Transaction:
    date_of_movement: datetime
    description: str
    value: int
    origin: str  # If it is CGD o BCP or other source
