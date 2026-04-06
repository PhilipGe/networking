class Interface:

    def __init__(self, name: str | None, ip: str, cidr: int):
        self.name = name
        self.ip = ip
        self.cidr = cidr
        self.sockets = {}
    
    def add_socket(self, socket):
        self.sockets.add(socket)