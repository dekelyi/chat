from _utils.hanlder import Handler


class MsgHandler(Handler):
    type = 'msg'

    def __init__(self, msg, user, *args, **kwargs):
        super(MsgHandler, self).__init__(*args, **kwargs)
        self.msg = msg
        self.user = user

    def process(self):
        print self.user, 'said:', self.msg
    