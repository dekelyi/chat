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
            with self.parent.lock:
                self.parent.socket_.send(utils.format_msg('msg', msg=reader.data[:-1]))
                write('\r')
                clearline()
            self.parent.queue.put(utils.format_msg('msg', msg=reader.data[:-1], user='YOU', _not_json=True))
            reader.data = ''

        # with self.parent.lock:
        #     clearline()
        #     write(reader.data)

