from __future__ import annotations
from dataclasses import dataclass


@dataclass
class Computer:
    def __init__(self, name: str, hacking_difficulty: int, hacked_value: int, risk_factor: float) -> None:
        self.name = name
        self.hacking_difficulty = hacking_difficulty
        self.hacked_value = hacked_value
        self.risk_factor = risk_factor

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Computer):
            return False
        return self.name == other.name and self.hacking_difficulty == other.hacking_difficulty and self.hacked_value == other.hacked_value and self.risk_factor == other.risk_factor

    def __hash__(self) -> int:
        return hash((self.name, self.hacking_difficulty, self.hacked_value, self.risk_factor))


    name: str
    hacking_difficulty: int
    hacked_value: int
    risk_factor: float
