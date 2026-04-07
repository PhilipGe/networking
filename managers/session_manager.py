import os

from entities.host import Host
import pty

from entities.service_enum import Service
from entities.socket import Socket
from translators.ssh_utils import flush_buffer

class CredentialManager:
    def __init__(self):
        self.bih_credentials = ('student', 'password')
        self.credentials = [
            ('net1_student5', 'password'),
            ('net1_comrade5', 'H00ld 73h d00r?'),
        ]

class Session:
    """
    Storage object for live sessions.
    session_type: str (Service.SSH,Service.TELNET)
    """
    def __init__(self, host: Host, fd):
        self.host = host
        self.fd = fd
    
    def submit(self, command, printBuf=False):
        command = command + ' && echo "ASDFGHJKL1234567890"'
        buffer = ''
        while True:
            try:
                data = os.read(self.fd, 1024)
                if(not data): break
                buffer += data.decode()
                if(printBuf): print(data.decode(), end='')
                if('ASDFGHJKL1234567890' in buffer): break
            except OSError:
                break
        return buffer

class TelnetSession(Session):

    def __init__(self, host, fd, socket, credential_manager: CredentialManager):
        super().__init__(host, fd)
        self.socket = socket
        self.credential_manager = credential_manager
        self.authenticate()
    
    def authenticate(self):
        pass

class SshSession(Session):

    def __init__(self, host, fd, socket, session_type, credential_manager: CredentialManager):
        super().__init__(host, fd)
        self.socket = socket
        self.credential_manager = credential_manager
        self.authenticate()
    
    def authenticate(self, username, password):
        os.write(self.fd, (f"ssh {username}@{self.socket.ip} -p {self.socket.port}" + '\n').encode())

        buffer = ''
        while not (('password' in buffer) or ('(yes/no)' in buffer)):
            try:
                data = os.read(self.fd, 1024)
                buffer += data.decode()
            except OSError:
                break
        
        if('(yes/no)' in buffer):
            os.write(self.fd, ('yes\n').encode())
            while not ('password' in buffer):
                try:
                    data = os.read(self.fd, 1024)
                    buffer += data.decode()
                    print(data.decode())
                except OSError:
                    break
            
        if('password' in buffer):
            os.write(self.fd, (password+'\n').encode())

        flush_buffer(self.fd, '$', printBuf=True)

class SessionManager:

    def __init__(self, bih: Host, credendial_manager):
        self.credential_manager = credendial_manager
        self.main_bih_session: Session = self._bih_init_shell(bih)
        self.ssh_session_map: dict[Host,Session] = {}
        self.telnet_session_map: dict[Host,Session] = {}

    def _bih_init_shell(self,bih):
        pid, fd = pty.fork()
        if(pid == 0):
            os.execvp('bash', ['bash'])
        else:
            self.main_bih_session = Session(bih, fd)
            return self.main_bih_session

    def init_ssh_session(self, host: Host) -> SshSession:
        pid, fd = pty.fork()
        if(pid == 0):
            os.execvp('bash', ['bash'])
        else:
            if(host.ssh_socket is None):
                print(f"No ssh socket on {host}. Unable to open session")
                return
            self.ssh_session_map[host] = SshSession(host, fd, host.ssh_socket, self.credential_manager)
            return self.ssh_session_map[host]

    def init_telnet_session(self, host: Host):
        pid, fd = pty.fork()
        if(pid == 0):
            os.execvp('bash', ['bash'])
        else:
            if(host.telnet_socket is None):
                print(f"No telnet socket on {host}. Unable to open session")
                return
            self.telnet_session_map[host] = fd