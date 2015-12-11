import chatterbot
chatbot = chatterbot.ChatBot("BergerBot", storage_adapter = "chatterbot.adapters.storage.JsonDatabaseAdapter")

import wolframalpha
import time
import os

import urllib2
import bs4

helpmsg = """
`!help` -- display this page

`!invite` -- display an invite link to this server

`!echo [message]` -- repeat `[message]` back to the user

`silentecho [message]` -- repeat `[message]` back to the user and erase the evidence

`!wolframalpha [query]` -- search Wolfram|Alpha for `[query]` and return the result

`!time` -- return the current time

`!date` -- return the current date

`!datetime` -- return both the current date and time

`!restart` -- restart bergerbot

`!xkcd` -- return the most recent xkcd comic

`!xkcd [number]` -- return comic number `number`

`!xkcd random` -- return any comic at random

__**ADMIN ONLY**__
`!train([conversation])` -- train bergerbot with a response to a certain phrase or set of phrases. Dialog is back-and-forth, with commas separating phrases

`!stop` -- stop the server
"""

inviteKey = "http://discord.gg/0geYLLHi71f9jF9j"
class ManualStopError(Exception):
    pass

class Command:
    def __init__(self):
        self.name = None
        self.roles = ["@everyone"]

    def execute(self):
        self.execution()
        return self.final_return()

    def execution(self):
        pass

    def final_return(self):
        return

####COMMANDS####
class helpme(Command):
    name="help"
    def __init__(self, args):
        self.roles = ["@everyone"]
    def final_return(self):
        return [["SAY", helpmsg]]

class train(Command):
    name="train"
    def __init__(self, args):
        self.roles = ["@admins"]
        self.args = args
    def execution(self):
        dialogue = self.args
        chatbot.train(dialogue)

class stop(Command):
    name="stop"
    def __init__(self, args):
        self.roles = ["@admins"]
    def execution(self):
        os.system("pm2 stop 0")
        raise ManualStopError

class invite(Command):
    name = "invite"
    def __init__(self, args):
        self.roles = ["@everyone"]
        self.args = args
    def final_return(self):
        return [["SAY",inviteKey]]
    
class echo(Command):
    name="echo"
    def __init__(self, args):
        self.roles = ["@everyone"]
        self.args = args
    def final_return(self):
        return [["SAY",self.args[0]]]

class silentecho(Command):
    name="silentecho"
    def __init__(self, args):
        self.roles = ["@everyone"]
        self.args = args
    def final_return(self):
        return [["DEL"],["SAY",self.args[0]]]
    
class WolframAlpha(Command):
    name = "wolframalpha"
    def __init__(self, args):
        self.roles = ["@everyone"]
        self.args = args
    def execution(self):
        waclient = wolframalpha.Client("TJJVVQ-7TJWQRP962")
        res = waclient.query(self.args[0])
        pods = [p.text.encode("utf-8") for p in res.pods if p.text is not None]
        self.returnstr = "\n\n".join(pods)
        
    def final_return(self):
        return [["SAY",self.returnstr]]

class Time(Command):
    name="time"
    def __init__(self, args):
        self.roles = ["@everyone"]
    def execution(self):
        self.time = time.strftime("%I:%M:%S %p")
    def final_return(self):
        return [["SAY", "Current time is "+self.time]]

class dateTime(Command):
    name="datetime"
    def __init__(self, args):
        self.roles = ["@everyone"]
    def execution(self):
        self.datetime = time.strftime("%Y-%m-%d %I:%M:%S %p")
    def final_return(self):
        return [["SAY", "Current date/time is "+self.datetime]]

class date(Command):
    name="date"
    def __init__(self, args):
        self.roles = ["@everyone"]
    def execution(self):
        self.date = time.strftime("%Y-%m-%d")
    def final_return(self):
        return [["SAY", "Current date is "+self.date]]

class restart(Command):
    name = "restart"
    def __init__(self, args):
        self.roles = ["@everyone"]
    def execution(self):
        os.system("pm2 restart 0")

class xkcd(Command):
    name="xkcd"
    def __init__(self, args):
        self.roles=["@everyone"]
        self.args = args
    def execution(self):
        inp = self.args[0]
        print "Input arg:", inp
        url='http://xkcd.com/'+str(inp)
        if inp is not None:
            if 'random' in inp:
                url = 'http://c.xkcd.com/random/comic/'
        elif inp is None:
            url='http://xkcd.com/'
        print "URL:",url

        try:
            soup = bs4.BeautifulSoup(urllib2.urlopen(url).read())
        except urllib2.HTTPError:
            self.fail = 1
            return

        comiclink = 'http:' + [s['src'] for s in soup.select('img') if 'imgs.xkcd.com/comics' in s['src']][0]
        self.extension = comiclink.split('.')[-1]
        comic = urllib2.urlopen(comiclink)
        with open('comic.'+self.extension,'w') as comicfile:
            comicfile.write(comic.read())
        self.fail = 0
    def final_return(self):
        if self.fail:
            return [['SAY', 'Comic not found']]
        else:
            return [['IMG', 'comic.'+self.extension], ['FDL','comic.'+self.extension]]


commands = {c.name:c for c in [helpme, train, stop, invite, echo, silentecho, WolframAlpha, Time, dateTime, date, restart, xkcd]}

cmdnames = commands.keys()

def processMsg(message, userRoles):
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
        print processMsg(raw_input(":"), ['@everyone'])
