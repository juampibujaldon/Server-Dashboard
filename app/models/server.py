from dataclasses import dataclass

@dataclass
class Server:
    name: str
    ip_address: str
    status: str
    id: str = None