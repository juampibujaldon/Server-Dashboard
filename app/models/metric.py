from dataclasses import dataclass, asdict

@dataclass
class Metric:
    serverId: str
    cpu_usage: float
    ram_usage: float
    disk_space: float
    temperature: float
    id: str = None

    def to_dict(self):
        return asdict(self)