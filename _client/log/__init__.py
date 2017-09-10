from ..connection import Connection
from _utils.term import PositionController

from . import msgs


class LogConn(Connection):
    handlers = [getattr(msgs, handler) for handler in msgs.__all__]
    
    def __init__(self, *args, **kwargs):
        super(LogConn, self).__init__(*args, **kwargs)

        self.pos = PositionController()
