import socket
import _socket
import select
from contextlib import contextmanager
import utils
from _utils.hanlder import Handler
from _utils.killable import KillableThread

# solves circular imports
# used only for type hinting
if __name__ == '__main__':
    from _client.main import MainConnection


class Connection(KillableThread):
    """
    async connection to the chat server

    :type _socket: _socket.socket
    :type parent: MainConnection
    :type conn: _socket.socket
    :type handlers: list[Handler]
    """
    handlers = []

    def __init__(self, parent, conn):
        """
        :param _socket.socket conn: connection details
        :type parent: MainConnection
        :param _socket.socket conn: socket to the conn connection process
        """
        super(Connection, self).__init__()

        self.parent = parent
        self.conn = conn

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

        may get {{context}} if {{self.contextmanager}} returns
        """
        lst = (self.conn,)
        with self.parent.lock:
            rlist, _, _ = select.select(lst, [], [], 0)
            all_data = [sock.recv(1024) for sock in rlist]
        for _data in all_data:  # type: basestring
            data = utils.parse_msg(_data)  # type: dict[basestring, any]
            args = data.get('args', ())
            try:
                del data['args']
            except KeyError:
                pass
            self.on_data(*args, **data)
    
    @contextmanager
    def contextmanager(self):
        yield

    def run(self):
        """
        main function
        """
        try:
            try:
                with self.contextmanager() as context:
                    while True:
                        args = () if context is None else (context,)
                        self.main(*args)
            except socket.error as err:
                print "ERROR:", err
            except (KeyboardInterrupt, SystemExit):
                pass
            finally:
                self.conn.send('EXIT')
        except socket.error as err:
            if err.errno != socket.errno.EBADF:
                raise
