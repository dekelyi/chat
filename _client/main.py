"""
main client program
"""
import socket
from select import select
import threading
import errno
import _socket  # pylint: disable=unused-import

import utils
from _client.connection import Connection


def _mock_socketpair(_server=None):
    if _server is None:
        tmp_server = socket.socket()
        tmp_server.bind(('localhost', 0))
        tmp_server.listen(1)
    else:
        tmp_server = _server

    tmp_server.setblocking(False)
    port = tmp_server.getsockname()[1]

    # Create non-blocking client socket
    client_sock = socket.socket()
    client_sock.setblocking(False)
    try:
        client_sock.connect(('localhost', port))
    except socket.error as err:
        # EWOULDBLOCK is not an error, as the socket is non-blocking
        if err.errno not in (errno.EWOULDBLOCK, errno.EINPROGRESS):
            raise

    # Use select to wait for connect() to succeed.
    timeout = 1
    readable = select([tmp_server], [], [], timeout)[0]
    if tmp_server not in readable:
        raise Exception('Client socket not connected in {} second(s)'.format(timeout))
    srv_sock, _ = tmp_server.accept()

    # close the server if needed
    if _server is None:
        tmp_server.close()

    return client_sock, srv_sock


class MainConnection(object):
    """
    :type addr: tuple
    :type lock: threading.Lock
    :type _socket: _socket.socket
    :type conn_server: _socket.socket
    :type connection: list[tuple[Connection, _socket.socket, _socket.socket]]
    """
    def __init__(self, addr):
        """
        :type addr: tuple
        """
        self.addr = addr
        self.lock = threading.Lock()

        self._socket = socket.socket()
        self._socket.connect(addr)

        self.conn_server = socket.socket()
        self.conn_server.bind(('localhost', 0))
        self.conn_server.listen(1)
        self.conn_server.setblocking(False)

        self.connections = []

    def add_connection(self, kls):
        """
        adds a connection handler
        :param type kls: subclass of Connection
        """
        server, client = _mock_socketpair(self.conn_server)
        conn = kls(self.lock, client)
        self.connections.append((conn, server))
        conn.start()

    def on_data(self, conn, data):
        """
        Send the data that arrived to all child connection excpet the sender

        :type conn: Connection
        :type data: basestring
        """
        if data == 'EXIT':
            raise SystemExit
        for connection in self.connections:
            if connection[0] is not conn:
                connection[1].send(data)

    def main(self):
        """
        main program loop
        """
        try:
            lst = [conn[1] for conn in self.connections] + [self._socket]
            while True:
                with self.lock:
                    rlist, _, _ = select(lst, [], [], 0)
                    rlist = [(sock, sock.recv(1024)) for sock in rlist]
                for sock, data in rlist:
                    conn = next((conn[0] for conn in self.connections if conn[1] is sock), self._socket)
                    self.on_data(conn, data)
        except (KeyboardInterrupt, SystemExit):
            raise SystemExit
