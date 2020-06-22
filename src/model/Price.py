from dataclasses import dataclass

@dataclass(frozen=True)
class Price:
    source: str
    price: int