from time import sleep
from _server.hanlder import TargetHandler, ThreadHandler, InvalidHandler


class MuteHandler(TargetHandler, ThreadHandler):
    type = 'mute'
    admin = True

    def __init__(self, target, time=3, *args, **kwargs):
        super(MuteHandler, self).__init__(target=target, *args, **kwargs)

        try:
            self.time = time = int(time)
        except ValueError:
            # will fail in the check
            pass

        if type(time) is not int or time <= 0:
            raise InvalidHandler('time must be an Integer greater than zero.')

    def run(self):
        try:
            self.target.muted = True
        except ValueError as err:
            raise InvalidHandler(err.message)

        self.conn.broadcast((self.target,), 'muted', user=str(self.target), by=str(self.user), time=self.time)
        self.target.send('muted', user='YOU', by=str(self.user), time=self.time)

        sleep(self.time * 60)

        UnmuteHandler.unmute(self, by='SYSTEM')


class UnmuteHandler(TargetHandler):
    type = 'unmute'
    admin = True
    def __init__(self, *args, **kwargs):
        super(UnmuteHandler, self).__init__(*args, **kwargs)
        if not self.target.muted:
            raise InvalidHandler('target is not muted')

    def process(self):
        UnmuteHandler.unmute(self, self.user)

    @staticmethod
    def unmute(self, by):
        self.target.muted = False

        self.conn.broadcast((self.target,), 'unmuted', user=str(self.target), by=str(by))
        self.target.send('unmuted', user='YOU', by=str(by))
