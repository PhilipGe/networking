class Interface:

    def __init__(self, name, ip, cidr):
        self.name = name
        self.ip = ip
        self.cidr = cidr
        self.sockets = {}
    
    def add_socket(self, socket):
        self.sockets.add(socket)