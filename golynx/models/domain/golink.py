from dataclasses import dataclass
from datetime import datetime


@dataclass
class Golink:
    link: str
    redirection: str
    created_by: str
    times_used: int = 0
    id: str | None = None
    created_at: datetime | None = None
