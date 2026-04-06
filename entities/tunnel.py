from entities.port import Socket

class Tunnel:

    def __init__(self, creator: Socket, forwarder: Socket, target: Socket):
        self.creator_socket = creator
        self.forwarder_socket = forwarder
        self.target_socket = target