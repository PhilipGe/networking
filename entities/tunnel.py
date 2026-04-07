class Tunnel:

    def __init__(self, authentication_socket, localhost_socket, target_socket):
        self.authentication_socket = authentication_socket
        self.localhost_socket = localhost_socket
        self.target_socket = target_socket