import ipaddress
import socket

from contextlib import closing

from wrapt import synchronized


@synchronized
def find_free_port_for_host(host):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    with closing(sock) as sock:
        sock.bind((host, 0))
        host, port = sock.getsockname()
        return port


def get_free_localhost_port():
    return find_free_port_for_host("localhost")


def is_in_private_network(host):
    host = socket.gethostbyname(host)
    ip_address = ipaddress.ip_address(host)
    private_networks = [
        "10.0.0.0/8",
        "172.16.0.0/12",
        "192.168.0.0/16",
    ]
    private_networks = [ipaddress.ip_network(network) for network in private_networks]
    for private_network in private_networks:
        if ip_address in private_network:
            return True
    return False
