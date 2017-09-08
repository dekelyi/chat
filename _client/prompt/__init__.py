from sys import stdout
import contextlib
import colorama

from ..connection import Connection
import utils
from _utils.reader import Reader
from _utils.term import clearline, write, position, TERMSIZE


class PromptConn(Connection):
    contextmanager = Reader

    def __init__(self, *args, **kwargs):
        super(PromptConn, self).__init__(*args, **kwargs)

        pos = list(TERMSIZE)
        pos[0] = 0
        position(*pos)

    def main(self, reader):
        """
        :param Reader reader: console reader object
        """
        super(PromptConn, self).main()

        reader.get_data()

        if reader.data.endswith('\n'):
            data = reader.data[:-1].strip()
            if data:
                with self.parent.lock:
                    self.parent.socket_.send(utils.format_msg('msg', msg=data))
                    self.parent.queue.put(utils.format_msg('msg', msg=data, user='YOU', _not_json=True))
            with self.parent.lock:
                write('\r')
                clearline()
            reader.data = ''
