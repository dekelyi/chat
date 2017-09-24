# pylint: disable=wrong-import-position,relative-import
from abc import ABCMeta, abstractmethod
import threading

from _server.user import User

# solves circular imports
# used only for type hinting
if __name__ == '__main__':
    from server import MultiUserServer  # pylint: disable=unused-import


class InvalidHandler(Exception):
    """
    A invalid command
    """
    pass


class Handler(object):
    """
    handle a message from the connection

    :type conn: MultiUserServer
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


class TargetHandler(Handler):
    def __init__(self, target, *args, **kwargs):
        super(TargetHandler, self).__init__(*args, **kwargs)
        self.target = User.get(target, self.conn.users)  # type: User

        if self.target is None:
            raise InvalidHandler('the target user does not logged in')

        if self.target == self.user:
            raise InvalidHandler('the target cannot be the user')
