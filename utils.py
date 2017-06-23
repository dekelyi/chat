"""
a utils library to both client and server
"""
import socket


def my_address():
    """
    :rtype: str
    :return: your local IP address
    """
    _sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    _sock.connect(('8.8.8.8', 0))
    ip = _sock.getsockname()[0]
    _sock.close()
    return ip


PREFIX = '!!SERVER!!: %s'  # type: str
