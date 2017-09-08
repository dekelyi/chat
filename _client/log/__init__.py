from ..connection import Connection
from _utils.positioner import Positioner

from . import msg


class LogConn(Connection):
    handlers = [msg.MsgHandler]
    
    def __init__(self, *args, **kwargs):
        super(LogConn, self).__init__(*args, **kwargs)

        self.pos = Positioner()
