from enum import Enum

class Service(Enum):
    SSH = "ssh"
    TELNET = "telnet"
    FTP = "ftp"
    HTTP = "http"