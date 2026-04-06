from entities.interface import Interface
from entities.port import Socket

class Host:

    def __init__(self):
        self.interfaces: set[Interface] = {}

    def add_interface(self, interface: Interface):
        self.interfaces.add(interface)