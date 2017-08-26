# pylint: disable=wrong-import-position,relative-import
from contextlib import contextmanager
from abc import ABCMeta, abstractmethod


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
        raise NotImplementedError


# solves circular imports
# used only for type hinting
if __name__ == '__main__':
    from connection import Connection  # pylint: disable=unused-import
