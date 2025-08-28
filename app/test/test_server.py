from models.server import Server

def test_server_creation_and_attributes():
    server_name = "web-server-01"
    server_ip = "192.168.1.100"
    server_status = "active"

    server = Server(name=server_name, ip_address=server_ip, status=server_status)

    assert server is not None
    assert server.name == server_name
    assert server.ip_address == server_ip
    assert server.status == server_status
    assert server.id is None  