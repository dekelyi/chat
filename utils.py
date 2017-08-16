"""
a utils library to both client and server
"""
import socket
import json
import collections


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


def format_msg(type_, *args, **kwargs):
    """
    :type type_: str
    """
    dct = {
        'type': type_,
        'args': args,
    }
    dct.update(kwargs)
    if isinstance(type_, collections.Mapping):
        # the type_ is the whole message
        dct = type_
    return json.dumps(dct)


def parse_msg(data):
    """
    :param str data: Message
    """
    return json.loads(data)
