from ..hanlder import Handler


class BaseMsgHandler(Handler):
    message = None

    def __init__(self, conn, *args, **kwargs):
        super(BaseMsgHandler, self).__init__(conn=conn)
        self.args = args
        self.kwargs = kwargs
        self.kwargs['type'] = self.type

    def process(self):
        if callable(self.message):
            self.message = self.message  # type: () -> Any
            msg = self.message(*self.args, **self.kwargs)
        elif isinstance(self.message, basestring):
            msg = self.message.format(*self.args, **self.kwargs)
        else:
            raise TypeError(".message must be a string or a function")

        with self.conn.parent.lock, self.conn.pos as pos:
            pos(msg)
    
