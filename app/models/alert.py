from dataclasses import dataclass, asdict

@dataclass
class Alert:
    serverId: str
    metric_type: str  # ej: "cpu_usage"
    threshold: float  # ej: 90.0
    condition: str    # ej: ">" o "<"
    id: str = None

    def to_dict(self):
        return asdict(self)