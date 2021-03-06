# pylint: disable=wrong-import-position,relative-import
from abc import ABCMeta, abstractmethod

# solves circular imports
# used only for type hinting
if __name__ == '__main__':
    from _client.connection import Connection  # pylint: disable=unused-import


class Handler(object):
    """
    handle a message from the connection

    :type conn: Connection
    :type type: basestring
    """
    __metaclass__ = ABCMeta
    type = ''

    def __init__(self, conn):
        """
        :type conn: Connection
        """
        self.conn = conn

    @abstractmethod
    def process(self):
        """
        hook to be called to handle the msg
        """
        raise NotImplementedError
