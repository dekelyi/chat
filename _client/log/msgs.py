from _base import BaseMsgHandler


class Message(BaseMsgHandler):
    type = 'msg'
    message = '{user} said: {msg}'


class InvalidCommand(BaseMsgHandler):
    type = 'invalid'
    message = '>> the command "{msg[type]}{msg[args]}" is invalid: {reason}.'


class UserJoined(BaseMsgHandler):
    type = 'joined'
    message = '!! {user} joined the chat.'


class UserLeft(BaseMsgHandler):
    type = 'left'
    message = '!! {user} left the chat.'


class UserKick(BaseMsgHandler):
    type = 'kicked'
    message = '!! {user} kicked out of the chat by {by}.'


class UserMute(BaseMsgHandler):
    type = 'muted'
    message = '!! {user} muted by {by} for {time} minutes.'


class UserUnmute(BaseMsgHandler):
    type = 'unmuted'
    message = '!! {user} unmuted by {by}.'


class IgnoredMuted(BaseMsgHandler):
    type = 'ignored_muted'
    message = '!! You Are Muted - message not sent !!'


__all__ = [
    'Message',
    'InvalidCommand',
    'UserJoined',
    'UserLeft',
    'UserKick',
    'UserMute',
    'UserUnmute',
    'IgnoredMuted'
]
