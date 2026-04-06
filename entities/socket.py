class Socket:
    
    def __init__(self, host, ip, port, service):
        self.host = host
        self.ip = ip
        self.port = port
        self.service = service

    def __str__(self):
        return f"{self.ip}:{self.port}"