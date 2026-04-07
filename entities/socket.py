class Socket:
    
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

    def on_localhost(self):
        return self.ip == '127.0.0.1' or self.ip == 'localhost'

    def __str__(self):
        return f"{self.ip}:{self.port}"