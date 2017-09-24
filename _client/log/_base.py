from ..hanlder import Handler


class BaseMsgHandler(Handler):
    message = None

    def __init__(self, *args, **kwargs):
        conn = kwargs['conn']
        del kwargs['conn']
        super(BaseMsgHandler, self).__init__(conn=conn)
        self.args = args
        self.kwargs = kwargs
        self.kwargs['type'] = self.type

    def process(self):
        if callable(self.message):
            self.message = self.message  # type: () -> Any
            msg = self.message(*self.args, **self.kwargs)
        elif isinstance(self.message, basestring):
            try:
                msg = self.message.format(*self.args, **self.kwargs)
            except (IndexError, KeyError):
                del self.kwargs['type']
                raise ValueError('"{0.type}" got wrong parameters: {0.args}{0.kwargs}'.format(self))
        else:
            raise TypeError("message must be a string or a function")

        with self.conn.parent.lock, self.conn.pos as pos:
            pos(msg)
    
