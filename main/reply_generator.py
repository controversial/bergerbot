import chatterbot
import os
from commands import *

def absolute(path):
    return os.path.join(os.path.dirname(os.path.abspath(__file__)),path)

chatbot = chatterbot.ChatBot("BergerBot",
                             storage_adapter = "chatterbot.adapters.storage.JsonDatabaseAdapter",
                             database=absolute("database.db"))
                             
set_train_bot(chatbot)
commands = {c.name:c for c in [helpme, train, stop, invite, echo, silentecho, WolframAlpha, Time, dateTime, date, restart, xkcd]}
cmdnames = commands.keys()


def processMsg(message, userRoles):
    print 'processing for channel bergerbot'
    if message.startswith('!'):
        inp = message[1:]
        for cn in cmdnames:
            if inp.startswith(cn):
                #Get command arguments
                args = inp[len(cn)+1:]
                if args.endswith(')'):
                    args = args[:-1].split(",")
                else:
                    args = args.split(",")

                #Actual instance of Command subclass
                cmdInstance = commands[cn](args)

                #CHECK PERMISSIONS
                #Roles which are allowed to execute command
                allowedRoles = cmdInstance.roles
                #Whether the command is allowed to be executed (If there is any intersection between userRoles and allowedRoles)
                allowed = any(i in allowedRoles for i in userRoles)
                #Execute command
                if allowed:
                    out = cmdInstance.execute()
                else:
                    out = [["SAY", "YOU SHALL NOT PASS!!!!!"]]

                return out

    #Otherwise generate chatbot response
    else:
        return [["SAY",chatbot.get_response(message)]]

if __name__ == '__main__':
    print 'ready'
    while 1:
        print processMsg(raw_input(":"), ['@admins'])
