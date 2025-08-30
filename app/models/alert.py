from dataclasses import dataclass, asdict

@dataclass
class Alert:
    serverId: str
    metric_type: str  
    threshold: float  
    condition: str   
    id: str = None

    def to_dict(self):
        return asdict(self)