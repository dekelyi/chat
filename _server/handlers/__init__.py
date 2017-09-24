from _server.hanlder import Handler
from . import msg, kick, mute

HANDLERS = [
    msg.MsgHandler,
    kick.KickHandler,
    mute.MuteHandler,
    mute.UnmuteHandler
]