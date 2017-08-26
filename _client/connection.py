import socket, _socket
import threading
import sys
import select
import utils
from .hanlder import Handler


class Connection(threading.Thread):
    """
    async connection to the chat server

    :type _socket: _socket.socket
    :type lock: threading.Lock
    :type parent: _socket.socket
    :type handlers: list[Handler]
    """
    handlers = []

    def __init__(self, conn, lock, parent):
        """
        :param _socket.socket | tuple conn: connection details
        :type lock: threading.Lock
        :param _socket.socket parent: socket to the parent connection process
        :raises TypeError: type don't match
        """
        super(Connection, self).__init__()

        self.lock = lock
        self.parent = parent

        if isinstance(conn, tuple):
            self._socket = socket.socket()
            self._socket.connect(conn)
        elif isinstance(conn, socket.socket):
            self._socket = conn
        else:
            raise TypeError("expected Tuple of Socket, found {}".format(type(conn)))

        self.on_init()

    def on_init(self):
        """
        hook to be called on initial of the client
        """
        pass

    def on_data(self, type, *args, **kwargs):
        """
        hook to be called when data is recived

        :type args: list[any]
        :type kwargs: dict[basestring, any]
        :rtype: bool
        :return: wheter or not the data is being used
        """
        kls = next((kls for kls in self.handlers if kls.type == type), None)
        if kls is None:
            return False

        handler = kls(*args, conn=self, **kwargs)  # type: Handler
        return handler.process()

    def main(self):
        """
        hook to be called as main loop program
        """
        lst = (self._socket, self.parent)
        while True:
            with self.lock:
                rlist, _, _ = select.select(lst, [], [], 0)
                all_data = [sock.recv(1024) for sock in rlist]
            for _data in all_data:  # type: basestring
                data = utils.parse_msg(_data)  # type: dict[basestring, any]
                args = data.get('args', ())
                try:
                    del data['args']
                except KeyError:
                    pass
                res = self.on_data(*args, **data)
                if res is False:
                    with self.lock:
                        self.parent.sendall(_data)

    def run(self):
        """
        main function
        """
        try:
            try:
                self.main()
            except socket.error as err:
                print "ERROR:", err
            except (KeyboardInterrupt, SystemExit):
                assert 0
                print "exitt"
            finally:
                self._socket.shutdown(socket.SHUT_RDWR)
                self._socket.close()
                self.parent.send('EXIT')
        except socket.error as err:
            if err.errno != socket.errno.EBADF:
                raise
