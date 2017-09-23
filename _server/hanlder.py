# pylint: disable=wrong-import-position,relative-import
from abc import ABCMeta, abstractmethod
import threading

from _server.user import User

# solves circular imports
# used only for type hinting
if __name__ == '__main__':
    from server import MultiUserServer  # pylint: disable=unused-import


class Handler(object):
    """
    handle a message from the connection

    :type type: basestring
    :type user_type: type | tuple[type]
    """
    __metaclass__ = ABCMeta
    type = ''
    user_type = User

    def __init__(self, user, conn):
        """
        :type conn: MultiUserServer
        :type user: User
        """
        self.conn = conn
        self.user = user

    @abstractmethod
    def process(self):
        """
        hook to be called to handle the msg
        """
        raise NotImplementedError


class ThreadHandler(Handler, threading.Thread):
    """
    A thread that acts via a Thread
    """
    def __init__(self, *args, **kwargs):
        threading.Thread.__init__(self)
        super(ThreadHandler, self).__init__(*args, **kwargs)

    def process(self):
        self.start()

    @abstractmethod
    def run(self):
        raise NotImplementedError
