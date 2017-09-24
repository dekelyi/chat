from time import sleep
from _server.hanlder import ThreadHandler


HELP = """----------------------------------------
Hello and welcome to the MultiUserChatApp - the MUCA.
write a message down there to sent it to the group.
write commands with ">>{name} [args1][ arg2][ arg3]...[ argN]"
- {required}
- [optional]
=======
>>admin {target}
Make a user an admin
=======
>>kick {target}
Kick the target out
=======
>>mute {target} [time]
mute target for {time:(3 defult)} minutes
=======
>>unmute {target}
unmute a muted target
----------------------------------------"""


class HelpHandler(ThreadHandler):
    type = 'help'

    def run(self):
        for line in HELP.split('\n'):
            self.user.send('msg', user='SYSTEM', msg=line)
            sleep(0.1)
