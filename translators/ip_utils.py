import pty
import re
import os

from entities.interface import Interface

def get_interfaces_from_ip_a():
    
    pid, fd = pty.fork()

    if pid == 0:
        os.execvp("bash", ["bash"])
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

    interfaces = []
    for m in matches:
        s = m.split(' ')
        ipv4wcidr = s[1].split('/')
        name = s[-1]
        ipv4 = ipv4wcidr[0]
        cidr = int(ipv4wcidr[1])
        interfaces.append(Interface(name, ipv4, cidr))
    
    return interfaces