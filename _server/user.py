import socket
import collections
import utils


class User(object):
    """
    Represent a user

    :type address: tuple
    :type client: socket.socket
    """

    def __init__(self, _socket, address, name=''):
        """
        :param socket.socket _socket: socket connection
        :param tuple address: (address[str], port[int])
        """
        self.address = address
        self.client = _socket

        self._muted = False
        self.admin = False
        self.name = name or ('%s:%i' % self.address)

    def send(self, type_, *args, **kwargs):
        """
        :param str data: base string (to format)
        :param Any args: args to format
        """
        msg = utils.format_msg(type_, *args, **kwargs)
        self.client.send(msg)

    def ask(self, question, rule=lambda x: True, users=None):
        """
        :type question: str
        :type users: list[User]
        """
        if users is None:
            users = [self]
        users.remove(self)
        res = ''
        while res is not None:
            new_question = question
            if res.strip():
                new_question = '%s (%s)' % (question, res)
            self.send('ask', question=new_question)
            data = utils.parse_msg(self.client.recv(1024))['answer']
            res = rule(data)
        users.append(self)
        return data

    @property
    def muted(self):
        return self._muted

    @muted.setter
    def muted(self, value):
        if type(value) is not bool:
            raise TypeError('type(muted) must be a Boolean')
        if self.admin and value:
            raise ValueError('Admin cannot be muted')
        self._muted = value

    def __str__(self):
        return ('@' if self.admin else '') + str(self.name)

    @staticmethod
    def get_sockets_from_users_list(lst):
        """
        :type lst: list[User]
        :type: list[socket.socket]
        """
        return [u.client for u in lst]

    @staticmethod
    def get_by_address(address, lst):
        """
        :type address: tuple
        :type lst: list[User]
        :rtype: User
        """
        return next((u for u in lst if u.address == address), None)

    @staticmethod
    def get_by_socket(_socket, lst):
        """
        :type _socket: socket.socket
        :type lst: list[User]
        :rtype: User
        """
        return next((u for u in lst if u.client is _socket), None)

    @staticmethod
    def get_by_name(name, lst):
        """
        :type name: basestring
        :type lst: list[User]
        :rtype: User
        """
        return next((u for u in lst if u.name == name), None)

    @staticmethod
    def get(user, lst):
        """
        :type user: Any
        :type lst: list[User]
        :rtype: User
        :raise TypeError: no reconginzed user identify method
        """
        if isinstance(user, socket.socket):
            return User.get_by_socket(user, lst)
        elif isinstance(user, basestring):
            return User.get_by_name(user, lst)
        elif isinstance(user, collections.Sequence):
            return User.get_by_address(user, lst)
        else:
            raise TypeError
