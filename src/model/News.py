from dataclasses import dataclass

@dataclass(frozen=True)
class News:
    source: str
    is_featured: bool