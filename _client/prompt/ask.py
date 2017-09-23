from ..hanlder import Handler
from _utils.term import clearline, write
from _utils.reader import Reader
from utils import format_msg


class askHandler(Handler):
    """
    hanlder to print messages
    """
    type = 'ask'

    def __init__(self, question, *args, **kwargs):
        super(askHandler, self).__init__(*args, **kwargs)
        self.question = question

    def process(self):
        write(self.question + ': ')
        with Reader() as reader:
            data = reader.read_line()
            clearline()
            
            msg = {
                'type_': 'answer',
                'question': self.question,
                'answer': data
            }

            self.conn.parent.socket_.send(format_msg(**msg))
