from dataclasses import dataclass, field


@dataclass
class Metmast:
    id: str = field(default=None)
    longitude: float = field(default=None)
    latitude: float = field(default=None)
