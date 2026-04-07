import pty
import re
import os

from entities.interface import Interface
from entities.socket import Socket
from entities.tunnel import Tunnel
from translators.subnet_calculator import address_space

def flush_buffer(fd, breakpattern=None, printBuf=False):
    buffer = ''
    while True:
        try:
            data = os.read(fd, 1024)
            if(not data): break
            buffer += data.decode()
            if(printBuf): print(data.decode(), end='')
            if((breakpattern is not None) and (breakpattern in buffer)): break
        except OSError:
            break
    return buffer

def get_interfaces_of_current_machine_from_ip_a():
    
    pid, fd = pty.fork()

    if pid == 0:
        os.execvp("ip", ["ip","a"])
    else:
        buffer = ''
        while True:
            try:
                data = os.read(fd, 1024)
                if not data:
                    break
                buffer += data.decode()
            except OSError:
                break
    
    matches: list[str] = re.findall(r'\n.*[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}.*\n',buffer)

    interfaces: list[Interface] = []
    for m in matches:
        s = m.split(' ')
        ipv4wcidr = s[1].split('/')
        name = s[-1]
        ipv4 = ipv4wcidr[0]
        cidr = int(ipv4wcidr[1])
        interfaces.append(Interface(name, ipv4, cidr))
    
    return interfaces

def get_interfaces_from_pty_shell(fd):
    os.write(fd, ('ip a\n').encode())

    buffer = flush_buffer(fd, '$', printBuf=True)
    matches: list[str] = re.findall(r'\n.*[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}.*\n',buffer)

    interfaces = []
    for m in matches:
        s = m.strip().split(' ')
        ipv4wcidr = s[1].split('/')
        name = s[-1]
        ipv4 = ipv4wcidr[0]
        cidr = int(ipv4wcidr[1])
        interfaces.append(Interface(name, ipv4, cidr))
    
    return interfaces

def _ssh_authenticate(fd,ssh_socket=None,username=None,password=None, added_flags=''):
    if(ssh_socket is not None): os.write(fd, (f"ssh {username}@{ssh_socket.ip} -p {ssh_socket.port} " + added_flags + '\n').encode())

    buffer = ''
    while not (('password' in buffer) or ('(yes/no)' in buffer)):
        try:
            data = os.read(fd, 1024)
            buffer += data.decode()
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

    flush_buffer(fd, '$', printBuf=True)

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

def scan_host_for_ips(fd, ip, ports):
    os.write(fd, f'./myscan.sh {ip} {ports}\n'.encode())
    buffer = flush_buffer(fd, 'done', True)
    matches: list[str] = re.findall(r'\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\] \d* ',buffer)

    socks: list[Socket] = []
    for m in matches:
        s = m.strip().split(' ')
        socks.append(Socket(
            None, s[0].replace('[','').replace(']',''), int(s[1]), None
        ))

    return socks

def scan_host(ssh_socket: Socket, username: str, password: str, ports='21-23 80') -> list[Socket]:
    """
    This can be ran off of BIH in order to capture machines exposed to a specific pivot. Exploration function. Returns a list of sockets
    """

    pid, fd = pty.fork()

    if pid == 0:
        os.execvp("bash", ["bash"])
    else:
        _ssh_authenticate(fd, ssh_socket, username, password, '-D 9050') # At this point the shell will be in the target machine's ssh, with a dynamic tunnel
        interfaces: list[Interface] = get_interfaces_from_pty_shell(fd) # This will get every interface of the new host

        pid2, fd2 = pty.fork()
        if pid2 == 0:
            os.execvp("bash", ["bash"])
        else:
            addresses = []
            for i in interfaces:
                if(i.ip == '127.0.0.1'): continue
                addresses += address_space(i.ip, i.cidr)
            
            found: list[Socket] = []
            for ip in addresses:
                ips_found = scan_host_for_ips(fd2, ip, ports)
                found += ips_found
            
            print(list(map(str, found)))
            return found
        
def open_socket_through_telnet(telnet_socket: Socket, pivot_ssh_socket: Socket, username: str, password: str):
    """
    Returns
        (telnet machine's localhost socket)
        (pivot's same interface ssh socket)
    """
    return 

def open_socket_through_ssh(telnet_socket: Socket, pivot_ssh_socket: Socket, username: str, password: str):
    """
    Returns
        (telnet machine's localhost socket)
        (pivot's same interface ssh socket)
    """
    return 