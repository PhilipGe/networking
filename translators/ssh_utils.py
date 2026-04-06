import pty
import re
import os

from entities.interface import Interface
from entities.port import Socket
from entities.tunnel import Tunnel

def _ssh_authenticate(fd, password):
    buffer = ''
    while not (('password' in buffer) or ('(yes/no)' in buffer)):
        try:
            data = os.read(fd, 1024)
            buffer += data.decode()
            print(data.decode())
        except OSError:
            break
    
    if('(yes/no)' in buffer):
        os.write(fd, ('yes\n').encode())
        while not ('password' in buffer):
            try:
                data = os.read(fd, 1024)
                buffer += data.decode()
                print(data.decode())
            except OSError:
                break
        
    if('password' in buffer):
        os.write(fd, (password+'\n').encode())

    while True:
        try:
            data = os.read(fd, 1024)
            if(not data): break
            print(data.decode())
        except OSError:
            break

def open_ssh_shell(ssh_socket: Socket, username: str, password: str):
    pid, fd = pty.fork()

    if pid == 0:
        os.execvp("ssh", ["ssh",f"{username}@{ssh_socket.ip}", "-p", f"{ssh_socket.port}"])
    else:
        _ssh_authenticate(fd, password)

def open_ssh_local_tunnel(tunnel: Tunnel, username: str, password: str):
    pid, fd = pty.fork()

    if pid == 0:
        os.execvp("ssh", [
            "ssh",f"{username}@{tunnel.forwarder_socket.ip}", "-p", f"{tunnel.forwarder_socket.port}",
            "-L",
            f"{tunnel.creator_socket.port}:{tunnel.target_socket.ip}:{tunnel.target_socket.port}",
            "-NT"
        ])
    else:
        _ssh_authenticate(fd, password)

def open_ssh_remote_tunnel(tunnel: Tunnel, username: str, password: str):
    pid, fd = pty.fork()

    if pid == 0:
        os.execvp("ssh", [
            "ssh",f"{username}@{tunnel.creator_socket.ip}", "-p", f"{tunnel.creator_socket.port}",
            "-R",
            f"{tunnel.forwarder_socket.port}:{tunnel.target_socket.ip}:{tunnel.target_socket.port}",
            "-NT"
        ])
    else:
        _ssh_authenticate(fd, password)