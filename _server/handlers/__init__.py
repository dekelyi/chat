from _server.hanlder import Handler
from . import msg, kick, mute, admin

HANDLERS = [
    msg.MsgHandler,
    kick.KickHandler,
    mute.MuteHandler,
    mute.UnmuteHandler,
    admin.AdminHandler
]