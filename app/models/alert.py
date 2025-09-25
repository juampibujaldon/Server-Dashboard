from dataclasses import dataclass, asdict
from typing import Optional

@dataclass
class Alert:
    serverId: str
    metric_type: str  
    threshold: float  
    condition: str   
    id: Optional[str] = None

    def to_dict(self):
        return asdict(self)
