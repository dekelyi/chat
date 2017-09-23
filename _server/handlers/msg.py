from _server.hanlder import Handler


class MsgHandler(Handler):
    type = 'msg'

    def __init__(self, msg, *args, **kwargs):
        super(MsgHandler, self).__init__(*args, **kwargs)
        self.msg = msg

    def process(self):
        data = {
            'type': 'msg',
            'user': str(self.user),
            'msg': self.msg
        }
        self.conn.broadcast(self.user, data)
