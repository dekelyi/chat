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
    # oh python3 - only keyword argumtns
    try:
        not_json = kwargs['_not_json']
        del kwargs['_not_json']
    except KeyError:
        not_json = False
    
    dct = {
        'type': type_.lower() if isinstance(type_, basestring) else type_,
        'args': args,
    }
    dct.update(kwargs)
    if isinstance(type_, collections.Mapping):
        # the {type_} is the whole message
        dct.update(type_)
    if not_json:
        return dct

    return json.dumps(dct)


def parse_msg(data):
    """
    :param str data: Message
    """
    obj = json.loads(data)

    try:
        obj['type'] = obj['type'].lower()
    except:
        pass
    
    return obj
