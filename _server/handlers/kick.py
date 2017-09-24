from _server.hanlder import TargetHandler


class KickHandler(TargetHandler):
    type = 'kick'

    def process(self):
        self.conn.remove_user(self.target, 'kicked', self.user)
