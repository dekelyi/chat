from _server.hanlder import Handler
from _server.user import User


class KickHandler(Handler):
    type = 'kick'

    def __init__(self, target, *args, **kwargs):
        super(KickHandler, self).__init__(*args, **kwargs)
        self.target = target

    def process(self):
        self.conn.remove_user(User.get(self.target, self.conn.users), 'kicked', self.user)
