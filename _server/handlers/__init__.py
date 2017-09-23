from _server.hanlder import Handler
from . import msg, kick

HANDLERS = [
    msg.MsgHandler,
    kick.KickHandler
]