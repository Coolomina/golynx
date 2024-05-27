from dataclasses import dataclass

@dataclass
class Golink:
    link: str
    redirection: str
    created_by: str
    times_used: int = 0