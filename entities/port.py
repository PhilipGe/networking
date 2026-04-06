from entities.host import Host
from entities.service_enum import Service

class Socket:
    
    def __init__(self, host: Host, ip: str, port: int, service: Service | None):
        self.host = host
        self.ip = ip
        self.ip = port
        self.service = service