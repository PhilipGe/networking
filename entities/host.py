from entities.socket import Socket

class Host:

    def __init__(self):
        self.ssh_socket = None
        self.telnet_socket = None
        self.http_socket = None
        self.ftp_socket = None

        self.all_sockets = []

    def get_next_free_localhost_socket(self):
        prefix = '105'
        localsockets = list(filter(lambda x: x.is_local(), self.all_sockets))
        localports = list(map(lambda x: x.port, localsockets))
        
        for i in range(99):
            p = prefix + str(i).zfill(2)
            if(p not in localports): break
        
        return Socket('127.0.0.1',p)

    def add_ssh_socket(self, socket: Socket):
        self.ssh_socket = socket
        self.all_sockets.append(socket)

    def add_telnet_socket(self, socket: Socket):
        self.telnet_socket = socket
        self.all_sockets.append(socket)

    def add_http_socket(self, socket: Socket):
        self.http_socket = socket
        self.all_sockets.append(socket)

    def add_ftp_socket(self, socket: Socket):
        self.ftp_socket = socket
        self.all_sockets.append(socket)

    def add_other_socket(self, socket: Socket):
        self.all_sockets.append(socket)