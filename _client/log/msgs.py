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


class UserLeft(BaseMsgHandler):
    type = 'kick'
    message = '!! {user} kicked out of the chat by {by}.'


__all__ = [
    'Message',
    'InvalidCommand',
    'UserJoined'
]
