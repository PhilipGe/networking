from entities.service_enum import Service
from translators.ssh_utils import *

if __name__ == '__main__':
    
    USERNAME = 'net1_student5'
    PASSWORD = 'password5'

    sock = Socket(None, '10.50.158.236', 7777, Service.SSH)
    # open_ssh_shell(sock, USERNAME, PASSWORD)
    scan_host(sock, USERNAME, PASSWORD, ports='21-23 80')