from _utils.hanlder import Handler


class MsgHandler(Handler):
    type = 'msg'

    def __init__(self, msg, user, *args, **kwargs):
        super(MsgHandler, self).__init__(*args, **kwargs)
        self.msg = msg
        self.user = user

    def process(self):
        with self.conn.parent.lock, self.conn.pos as pos:
            pos(self.user, 'said:', self.msg)
    