from entities.host import Host
from entities.interface import Interface
from entities.tunnel import Tunnel
from managers.session_manager import SessionManager
from network_graph import NetworkGraph
from translators.ssh_utils import get_interfaces_of_current_machine_from_ip_a, open_ssh_local_tunnel, scan_host

USERNAME = 'net1_student5'
PASSWORD = 'password5'

def explore_graph_well_known(bih: Host, pivot: Host, netgraph: NetworkGraph, session_manager: SessionManager):
    """
        BIH is the machine that has all tool available to it
        pivot is the machine that can be ssh'd into from BIH and explored as a proxy
        every new socket found from proxy is consolidated into seperate hosts
        every host that has an ssh socket open is tunnelled to
        every host that has a telnet socket open is reverse tunelled to

        the hosts' ssh sockets are marked as unexplored
    """
    netgraph.register_host(pivot)
    if(len(pivot.interfaces) == 0): return netgraph
    
    # (1) Set up dynamic proxy
    if(pivot.ssh_socket is None): return netgraph
    
    # (2) Scan host on all interfaces for various sockets found
    sockets_found = scan_host(pivot.ssh_socket, USERNAME, PASSWORD)
    
    # (3) Consolidate into hosts
    host_dict: dict[str, Host] = {}
    for s in sockets_found:
        if(s.ip not in host_dict.keys()): host_dict[s.ip] = Host()
        if(s.port == 22): host_dict[s.ip].add_ssh_socket(s)
        elif(s.port == 80): host_dict[s.ip].add_http_socket(s)
        elif(s.port == 23): host_dict[s.ip].add_ftp_socket(s)
        elif(s.port == 23): host_dict[s.ip].add_telnet_socket(s)
        else: host_dict[s.ip].add_other_socket(s)
    
    # (4) Register hosts with network graph, storing
        # ssh daemons
        # telnet daemons
        # ftp servers
        # http servers
    hosts = set(host_dict.values())
    for h in hosts: netgraph.register_host(h)
    
    # (5) Set up tunnel through pivot to ssh daemons
    for h in hosts:
        if(h.ssh_socket is not None): 
            ssh_session = session_manager.init_ssh_session(h)
            ssh_session.submit()
        elif(h.telnet_socket is not None):
            pass
            
        # (5.1) If only telnet is exposed, log in through telnet, set up remote tunnel to pivot, set up local tunnel to BIH

    # (6) Reap http and ftp servers
        elif(h.http_socket is not None): session_manager.main_bih_session.submit(f'proxychains wget -r http://{h.http_socket.ip}:{h.http_socket.port}')
        elif(h.ftp_socket is not None): session_manager.main_bih_session.submit(f'proxychains wget -r ftp://{h.ftp_socket.ip}:{h.ftp_socket.port}')

    # (7) If telnet:
        # Log in to telnet
        # Set up the remote tunnel
        # Set up tunnel to 
    
    frontier = [*pivot.interfaces]

    while frontier:
        currint: Interface = frontier.pop(0)
