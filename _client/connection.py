import socket
import _socket
import select
import contextlib
import Queue
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

    :type parent: MainConnection
    :type handlers: list[Handler]
    """
    handlers = []

    def __init__(self, parent):
        """
        :type parent: MainConnection
        """
        super(Connection, self).__init__()
        self.name = str(self)

        self.parent = parent

        self.on_init()

    def on_init(self):
        """
        hook to be called on initial of the client
        """
        pass

    def on_data(self, type_, *args, **kwargs):
        """
        hook to be called when data is recived

        :param str type_: type of message
        :type args: list[any]
        :type kwargs: dict[basestring, any]
        :rtype: bool
        :return: wheter or not the data is being used
        """
        kls = next((kls for kls in self.handlers if kls.type == type_), None)
        if kls is None:
            return False

        handler = kls(*args, conn=self, **kwargs)  # type: Handler
        return handler.process()

    def main(self):
        """
        hook to be called as main loop program

        may get {{context}} if {{self.contextmanager}} returns
        """
        try:
            data = self.parent.queue.get_nowait()  # type: dict[basestring, any]
            data_conn = data.get('_conn', [])

            try:
                del data['_conn']
            except KeyError:
                pass

            if self not in data_conn:
                args = data.get('args', ())
                try:
                    del data['args']
                except KeyError:
                    pass

                type_ = data['type']
                del data['type']

                res = self.on_data(type_, *args, **data)
                data['args'] = args
                data['_conn'] = data_conn + [self]
                data['type'] = type_
            else:
                res = False
            if res is False:
                self.parent.queue.put(data)
            self.parent.queue.task_done()
        except Queue.Empty:
            pass
    
    @contextlib.contextmanager
    def contextmanager(self):
        """
        Context manager to be called on the main program
        """
        yield

    def run(self):
        """
        main function
        """
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
            self.parent.exit = True
