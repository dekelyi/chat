from ..connection import Connection

from . import msg


class LogConn(Connection):
    handlers = [msg.MsgHandler]