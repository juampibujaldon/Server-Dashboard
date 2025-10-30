from dataclasses import dataclass, asdict
from typing import Optional

@dataclass
class Metric:
    server_id: str
    cpu_usage: float
    ram_usage: float
    disk_space: float
    temperature: float
    sent_at: Optional[str] = None
    id: Optional[str] = None

    def to_dict(self):
        return asdict(self)
