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


def format_msg(type_, msg):
    """
    :type type_: str
    :type msg: str
    """
    if type_ == 'sys':
        return PREFIX % (msg,)
    return msg


def parse_msg(data):
    """
    :param str data: Message
    """
    type_ = 'sys' if data.startswith(PREFIX % '') else 'msg'
    msg = data.replace(PREFIX % '', '')
    if type_ == 'msg' and not msg.strip():
        return {}
    return {'type': type_, 'msg': msg}
