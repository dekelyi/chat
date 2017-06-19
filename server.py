#!/usr/bin/env python2
# coding=utf-8
"""

"""
import socket
from select import select
from sys import argv, stdout
from os import name as os

PREFIX = '!!SERVER!!: %s'  # type: str


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

    def send(self, data, *args):
        """
        :param str data: base string (to format)
        :param Any args: args to format
        """
        self.client.send((data + '\n') % args)

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
        try:
            return [u for u in lst if u.address == address][0]
        except IndexError:
            return None

    @staticmethod
    def get_by_socket(_socket, lst):
        """
        :type _socket: socket.socket
        :type lst: list[User]
        :rtype: User
        """
        try:
            return [u for u in lst if u.client is _socket][0]
        except IndexError:
            return None

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
    prefix = PREFIX

    def __init__(self, port, listen):
        self.server = _server = socket.socket()  # type: socket.socket
        _server.bind(('', port))
        _server.listen(listen)
        print 'Listening on %s:%i to %i connections' % (my_address(), port, listen)
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
        """
        try:
            if type(user) != User:
                user = User.get(user, self.users)
            user.client.close()
            self.users.remove(user)
            print '%s disconnected' % user
        except (IndexError, ValueError):
            print '!! Error !!'

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
        user.send(self.prefix, 'data received')
        self.broadcast(data, user)

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
        except Exception as e:
            print 'Error occurred, disconnected.'
            self.server.close()

    def broadcast(self, data, exclude=()):
        """
        broadcast a message to all user, except {exclude}
        :param data: string to send, or [function(User user) -> str] to send her return.
        :type data: str | (User) -> str
        :param exclude: list[User] | User
        """
        if not hasattr(exclude, '__iter__'):
            exclude = [exclude]
        users = [u for u in self.users if u not in exclude]
        MultiUserServer.send_to(users, data)

    @staticmethod
    def send_to(users, data):
        """
        send a message to {users}
        :type users: list[User]
        :param data: string to send, or [function(User user) -> str] to send her return.
        :type data: str | (User) -> str
        """
        for u in users:
            u.send(data if not callable(data) else data(u))


def my_address():
    """
    :rtype: str
    :return: your local IP address
    """
    _sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    _sock.connect(('8.8.8.8', 0))
    ip = _sock.getsockname()[0]
    _sock.close()
    return ip


PORT = 8001


def main():
    """
    server demo
    """
    _server = MultiUserServer(PORT, 2)
    _server.main()


if __name__ == '__main__':
    main()
