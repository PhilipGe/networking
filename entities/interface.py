
from entities.port import Socket

class Interface:

    def __init__(self, name: str | None, ip: str, cidr: int):
        self.name = name
        self.ip = ip
        self.cidr = cidr
        self.sockets: set[Socket] = {}
    
    def add_socket(self, socket: Socket):
        self.sockets.add(socket)