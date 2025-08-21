from models.server import Server

def test_server_creation_and_attributes():
    """
    Prueba la creación de un objeto Server y verifica sus atributos.
    """
    # 1. Preparación (Arrange)
    # Definimos los datos que usaremos para crear el objeto.
    server_name = "web-server-01"
    server_ip = "192.168.1.100"
    server_status = "active"

    # 2. Actuación (Act)
    # Creamos una instancia de la clase Server.
    server = Server(name=server_name, ip_address=server_ip, status=server_status)

    # 3. Afirmación (Assert)
    # Verificamos que el objeto se haya creado y que los atributos
    # tengan los valores correctos.
    assert server is not None
    assert server.name == server_name
    assert server.ip_address == server_ip
    assert server.status == server_status
    assert server.id is None  # Verificamos que el valor por defecto es None