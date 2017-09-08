from ..connection import Connection
from _utils.term import PositionController

from . import msg
from . import invalid


class LogConn(Connection):
    handlers = [
        msg.MsgHandler,
        invalid.invalidHandler
    ]
    
    def __init__(self, *args, **kwargs):
        super(LogConn, self).__init__(*args, **kwargs)

        self.pos = PositionController()
