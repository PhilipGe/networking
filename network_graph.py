from typing import Tuple

from entities.host import Host
from entities.port import Socket
from entities.tunnel import Tunnel

class NetworkGraph:

    def __init__(self):
        self.edges: set[frozenset[Socket, Socket]] = {}
    
    def register_host(self):
        pass