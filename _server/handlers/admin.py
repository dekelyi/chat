from _server.hanlder import TargetHandler


class AdminHandler(TargetHandler):
    type = 'admin'
    admin = True

    def process(self):
        self.target.admin = True

        self.conn.broadcast((self.target,), 'adminized', user=str(self.target), by=str(self.user))
        self.target.send('adminized', user='YOU', by=str(self.user))
