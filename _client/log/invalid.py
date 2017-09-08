from _utils.hanlder import Handler


class invalidHandler(Handler):
    """
    hanlder to print messages
    """
    type = 'invalid'

    def __init__(self, msg, reason, *args, **kwargs):
        super(invalidHandler, self).__init__(*args, **kwargs)
        self.msg = msg
        self.reason = reason

    def process(self):
        with self.conn.parent.lock, self.conn.pos as pos:
            pos('>> The command', self.msg, 'is invalid:', self.reason)
    