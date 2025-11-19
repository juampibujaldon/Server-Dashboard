from dataclasses import asdict, dataclass
from typing import Optional


@dataclass
class Alert:
    server_id: str
    metric_type: str  
    threshold: float  
    condition: str   
    id: Optional[str] = None

    def to_dict(self):
        return asdict(self)
