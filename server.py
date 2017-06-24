#!/usr/bin/env python2
# coding=utf-8
"""

"""
import socket
from select import select
from sys import stdout
import utils
import config


class User:
    """
    used by MultiUserServer to represent a single user
    .. to be inherited
    :type address: tuple
    :type client: socket.socket
    """

    def __init__(self, _socket, address):
        """
        :param socket.socket _socket: socket connection
        :param tuple address: (address[str], port[int])
        """
        self.address = address
        self.client = _socket

    def send(self, type_, *args, **kwargs):
        """
        :param str data: base string (to format)
        :param Any args: args to format
        """
        self.client.send(utils.format_msg(type_, *args, **kwargs))

    def __str__(self):
        return '%s:%i' % (self.address[0], self.address[1])

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
    def get(user, lst):
        """
        :type user: Any
        :type lst: list[User]
        :rtype: User
        """
        if type(user) == socket.socket:
            return User.get_by_socket(user, lst)
        elif type(user) == tuple:
            return User.get_by_address(user, lst)


class MultiUserServer:
    """
    a chat-like server that support multiple user, in a non-blocking async way
    .. to be inherited
    :type users: list[User]
    :type server: socket.socket
    """

    def __init__(self, port, listen):
        self.server = _server = socket.socket()  # type: socket.socket
        _server.bind(('', port))
        _server.listen(listen)
        print 'Listening on %s:%i to %i connections' % (utils.my_address(), port, listen)
        self.users = []

    def add_user(self, *args):
        """
        adds a user to the users list
        .. do additional things
        .. to be overridden
        :param args: a User object, or the parameters to a User object
        :type args: User | list
        """
        if type(args[0]) == User:
            user = args[0]
        else:
            user = User(*args)
        print '%s connected' % user
        self.users.append(user)

    def remove_user(self, user):
        """
        removes user from the users list
        .. do additional things
        .. to be overridden
        :param user: a User object, or some sort of ID to User.get() method
        :type user: User | Any
        :raise Exception: user doesnt exist
        """
        if not isinstance(user, User):
            user = User.get(user, self.users)
            if not user:
                raise Exception('user doesnt exist')
        user.client.close()
        self.users.remove(user)
        print '%s disconnected' % user

    def read(self, user, data):
        """
        process data sent from user
        .. do additional things
        .. to be overridden
        :param User user: user.
        :param str data: data.
        """
        print '-',
        stdout.flush()
        user.send('sys', 'data received')
        self.broadcast(user, 'msg', data,)

    def main(self):
        """
        do main processing of the server
        """
        try:
            while True:
                lst = [self.server] + User.get_sockets_from_users_list(self.users)
                r, _, _ = select(lst, lst, lst)
                for sock in r:
                    if sock is self.server:
                        self.add_user(*self.server.accept())
                    else:
                        user = User.get_by_socket(sock, self.users)
                        try:
                            data = sock.recv(1024)
                        except socket.error:
                            data = ''
                        if data == '':
                            self.remove_user(sock)
                        else:
                            self.read(user, data)
        except Exception:
            raise

    def broadcast(self, exclude, type_, *args, **kwargs):
        """
        broadcast a message to all user, except {exclude}
        :param exclude: list[User] | User
        :type type_: str
        :type args: list[object]
        :type kwargs: dict[str, object]
        """
        if not hasattr(exclude, '__iter__'):
            exclude = exclude,
        users = (u for u in self.users if u not in exclude)
        MultiUserServer.send_to(users, type_, *args, **kwargs)

    @staticmethod
    def send_to(users, type_, *args, **kwargs):
        """
        send a message to {users}
        :type users: list[User]
        :type type_: str
        :type args: list[object]
        :type kwargs: dict[str, object]
        """
        for u in users:
            u.send(type_, *args, **kwargs)


def main():
    """
    server demo
    """
    _server = MultiUserServer(config.PORT, 2)
    _server.main()


if __name__ == '__main__':
    main()
