from _base import BaseMsgHandler


class Message(BaseMsgHandler):
    type = 'msg'
    message = '{user} said: {msg}'


class InvalidCommand(BaseMsgHandler):
    type = 'invalid'
    message = 'the command ">> {msg[type]}{msg[args]}" is invalid: {reason}'

__all__ = [
    'Message',
    'InvalidCommand'
]