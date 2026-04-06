x32MASK = 0xffffffff

def ipv4_str_to_hex(addr: str):
    octets = addr.split('.')
    networkashex = 0
    for i in range(4):
        networkashex = networkashex | (int(octets[i]) << (3-i)*8)
    return networkashex

def ipv4_hex_to_str(networkashex: str):
    octets = []
    for i in range(4):
        m = 0xff << (3-i)*8
        a = networkashex & m
        octets.append(str(a >> (3-i)*8))
    return '.'.join(octets)

def address_space(addr: str, cidr: int):
    addr_as_hex = ipv4_str_to_hex(addr)
    netmask = x32MASK & (x32MASK << (32 - cidr))
    hostmask = (~netmask) & x32MASK
    
    netaddr = addr_as_hex & netmask
    lastnetaddr = netaddr + hostmask

    return list(map(ipv4_hex_to_str, range(netaddr, lastnetaddr+1)))