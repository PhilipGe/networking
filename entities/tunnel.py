class Tunnel:

    def __init__(self, creator, forwarder, target):
        self.creator_socket = creator
        self.forwarder_socket = forwarder
        self.target_socket = target