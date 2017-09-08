from sys import stdout
import contextlib
import colorama
from functools import partial

from ..connection import Connection
import utils
from _utils.reader import Reader
from _utils.term import clearline, write, position, TERMSIZE

from . import ask


class PromptConn(Connection):
    contextmanager = Reader
    handlers = [
        ask.askHandler
    ]

    def __init__(self, *args, **kwargs):
        super(PromptConn, self).__init__(*args, **kwargs)

        pos = list(TERMSIZE)
        pos[0] = 0
        position(*pos)

    def _get_format(self, data):
        """
        get format function to the appropiate {{data}}

        :type data: str
        """
        type_, args, kwargs = '', [], {}
        if data.startswith('>>'):
            args = data[2:].split(' ')
            type_ = args[0]
            del args[0]
        else:
            type_ = 'msg'
            kwargs['msg'] = data
        return partial(utils.format_msg, type_, *args, **kwargs)

    def main(self, reader):
        """
        :param Reader reader: console reader object
        """
        super(PromptConn, self).main()

        reader.get_data()

        if reader.data.endswith('\n'):
            data = reader.data[:-1].strip()
            if data:
                format_msg = self._get_format(data)
                with self.parent.lock:
                    self.parent.socket_.send(format_msg())
                    self.parent.queue.put(format_msg(user='YOU', _not_json=True))
            with self.parent.lock:
                write('\r')
                clearline()
            reader.data = ''
