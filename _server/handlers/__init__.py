from _server.hanlder import Handler
from . import msg, kick, mute, admin, help

HANDLERS = [
    msg.MsgHandler,
    kick.KickHandler,
    mute.MuteHandler,
    mute.UnmuteHandler,
    admin.AdminHandler,
    help.HelpHandler
]