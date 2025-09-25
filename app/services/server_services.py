from typing import Dict, List, Any, Optional
from app.models.server import Server
from dataclasses import asdict
from app.repositories.servers_repo import ServersRepository as Repo


def create_server(server: Server) -> str:
    return Repo.insert(asdict(server))


def get_server_by_id(server_id: str) -> Optional[Dict[str, Any]]:
    return Repo.get_by_id(server_id)


def list_servers() -> List[Dict[str, Any]]:
    return Repo.list_all()


def update_server(server_id: str, updates: Dict[str, Any]) -> int:
    return Repo.update(server_id, updates)


def delete_server(server_id: str) -> int:
    return Repo.delete(server_id)
