import socket
from contextlib import closing

from wrapt import synchronized


@synchronized
def find_free_port_for_host(host=None):
    if host is None:
        host = "localhost"
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
        sock.bind((host, 0))
        host, port = sock.getsockname()
        return port


def get_free_localhost_port():
    return find_free_port_for_host("localhost")
