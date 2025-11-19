from dataclasses import dataclass
from typing import Optional


@dataclass
class Server:
    name: str
    ip_address: str
    status: str
    id: Optional[str] = None
