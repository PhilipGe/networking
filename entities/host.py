class Host:

    def __init__(self):
        self.interfaces = {}

    def add_interface(self, interface):
        self.interfaces.add(interface)