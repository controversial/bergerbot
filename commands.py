"""Implements all of the Commands used by bergerbot,
as well as an interface for implementing new ones

The structure of a Command should be something like:
[["SAY","message"],["IMG","path_to_image.jpg"]]

The final_return of a Command should return a list, each item of which
is another list containing an operation and sometimes some arguments.

Recognized operations are:
SAY: send a message containing the text passed as an argument
    Example: ["SAY", "Hello"]
IMG: send a file located at the path passed as an argument
    Example: ["IMG", "cat.png"]
FDL: delete a file located as the path passed as an argument
    Example: ["FDL", "unnecessary"]
DEL: delete the message which the Command is replying to
    Example:["DEL"]

More complete examples of how to use this system are included below
"""


####GLOBALS####
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


import wolframalpha
import time
import os
import urllib2
import bs4




####BASIC INTERFACE####
class Command:
    """The basic command class. All commands should inherit from this,
       replacing name, execution, and final_return. When your command is
       executed, `execute` will be run. Typical usage is to subclass
       execution, final_return, and __init__ but not execute"""
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


def set_train_bot(bot):
    global chatbot
    chatbot = bot
    
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
        raise Exception



class invite(Command):
    name = "invite"
    def __init__(self, args):
        self.roles = ["@everyone"]
        self.args = args
    def final_return(self):
        return [["SAY","http://discord.gg/0geYLLHi71f9jF9j"]]


    
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
