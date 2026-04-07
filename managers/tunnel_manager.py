from entities.socket import Socket


class TunnelManager:
    
    def __init__(self):
        self.tunnels = []

    def create_local_tunnel(self, forwarder_socket: Socket, local_port: int, target_socket: Socket):
        pass

    def create_remote_tunnel_through_telnet(
            self,
            pivot_ssh_socket: Socket,
            target_telnet_socket: Socket,
            bih_local_port: int,
            pivot_local_port: int,
            target_local_ssh_port: int
    ):  
        pass