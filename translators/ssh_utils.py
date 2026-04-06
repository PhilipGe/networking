import pty
import re
import os

from entities.interface import Interface
from entities.port import Socket

def open_ssh_shell(ssh_socket: Socket, username: str, password: str):
    pid, fd = pty.fork()

    if pid == 0:
        os.execvp("ssh", ["ssh",f"{username}@{ssh_socket.ip} -p {ssh_socket.port}"])
    else:
        buffer = ''
        while not ('password' in buffer):
            try:
                data = os.read(fd, 1024)
                buffer += data.decode()
            except OSError:
                break
        
        if('password' in buffer):
            os.write(fd, password)

        while True:
            try:
                data = os.read(fd, 1024)
                if(not data): break
                print(data.decode)
            except OSError:
                break