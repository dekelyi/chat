#!/usr/bin/env python2
# coding=utf-8
"""
Server application
"""
import socket
import threading
from select import select
from sys import stdout, exit as sys_exit
import utils
import config
from _server.user import User
from _server.handlers import Handler, HANDLERS


class MultiUserServer(object):
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
        :type args: User | any
        """
        def _ask_name(_user):
            # solve blocking name-asking
            user.name = user.ask('name', None)
            print '%s connected' % user
            self.broadcast((), 'joined', user=str(user))
        
        if isinstance(args[0], User):
            user = args[0]
        else:
            user = User(*args)
        # oh my sweet python3's async and await - i could use you so much right now.
        # i hate threads.
        threading.Thread(target=_ask_name, args=(user,)).start()
        self.users.append(user)

    def remove_user(self, user, reason='left', by=None):
        """
        removes user from the users list
        .. do additional things
        .. to be overridden
        :param user: a User object, or some sort of ID to User.get() method
        :type user: User | any
        :raise Exception: user doesnt exist
        """
        if not isinstance(user, User):
            user = User.get(user, self.users)
            if not user:
                raise Exception('user doesnt exist')
        
        more_kwargs = {}
        if by:
            more_kwargs['by'] = str(by)

        user.client.close()
        self.users.remove(user)
        print '%s disconnected: %s by %s' % (user, reason, by)
        self.broadcast((), reason, user=str(user), **more_kwargs)

    def read(self, user, data):
        """
        process data sent from user
        .. do additional things
        .. to be overridden
        :param User user: user.
        :param str data: data.
        """
        stdout.flush()
        type_ = data['type']
        del data['type']
        kls = next((kls for kls in HANDLERS if kls.type == type_), None)
        if kls:
            try:
                args = data['args']
                del data['args']
            except KeyError:
                args = ()
            handler = kls(*args, user=user, conn=self, **data)
            handler.process()
        else:
            data['type'] = type_
            user.send('invalid', msg=data, reason='Unkown type of command')

    def main(self):
        """
        do main processing of the server
        """
        try:
            while True:
                lst = [self.server] + User.get_sockets_from_users_list(self.users)
                rlist, _, xlist = select(lst, lst, lst)
                for sock in rlist + xlist:
                    if sock is self.server:
                        self.add_user(*sock.accept())
                    else:
                        user = User.get_by_socket(sock, self.users)
                        if sock in xlist:
                            data = ''
                        else:
                            try:
                                data = sock.recv(1024)
                            except socket.error:
                                data = ''
                        if data == '':
                            self.remove_user(sock)
                        else:
                            self.read(user, utils.parse_msg(data))
        except (KeyboardInterrupt, SystemExit):
            pass
        finally:
            print "Server shutdown..."
            for user in self.users:  # type: User
                self.remove_user(user, reason='shutdown', by='SYSTEM')
            self.server.close()
            sys_exit(0)

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
        for usr in users:
            usr.send(type_, *args, **kwargs)


def main():
    """
    server demo
    """
    _server = MultiUserServer(config.PORT, 2)
    _server.main()


if __name__ == '__main__':
    main()
