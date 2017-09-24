from _server.hanlder import TargetHandler


class KickHandler(TargetHandler):
    type = 'kick'
    admin = True

    def process(self):
        self.conn.remove_user(self.target, 'kicked', self.user)
