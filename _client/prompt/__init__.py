from ..connection import Connection
from _utils.reader import Reader
import utils
from sys import stdout


class PromptConn(Connection):
    contextmanager = Reader

    def main(self, reader):
        """
        :param Reader reader: console reader object
        """
        reader.get_data()
        if reader.data.endswith('\n'):
            with self.parent.lock:
                self.parent._socket.send(utils.format_msg('msg', msg=reader.data[:-1]))
            stdout.write('\r')
            stdout.flush()
            self.conn.send(utils.format_msg('msg', msg=reader.data[:-1], user='YOU'))
            reader.data = ''
        super(PromptConn, self).main()
