import discord
import random
import time
import traceback
import os

from reply_generator import processMsg

client = discord.Client()
client.login('ldt@deentaylor.com', 'bergers4days')

with open('discord_log.txt', 'a') as log:
    log.write("\nMANUAL RESTART "+time.strftime("%Y-%m-%d %H:%M:%S"))

####Main function for handling command responses####
def cmdHandle(client, message):
    server, channel, member = message.server, message.channel, message.author
    user = client.user

    #user's roles (for permissions)
    userRoles = [r.name for r in member.roles]
    #Processs properly structured response
    cmds = processMsg(message.content, userRoles)
    if cmds:
        for c in cmds:
            if c[0] == "DEL":
                client.delete_message(message)
            elif c[0] == "SAY":
                client.send_message(channel, c[1])
            elif c[0] == "IMG":
                client.send_file(message.channel, c[1])
            elif c[0] == "FDL":
                os.remove(c[1])
            
@client.event
def on_ready():
    print 'Connected as', client.user.name
    with open('discord_log.txt', 'a') as log:
        log.write("\nSTART "+time.strftime("%Y-%m-%d %H:%M:%S"))
        global inittime
        inittime = time.time()

    servers = client.servers
    botserver = servers[[s.name for s in servers].index("bergerbot")]
    channels = botserver.channels
    botchannel = channels[[c.name for c in channels].index("bergerbot")]
    wakeups = ["Bergerbot is up and running",
               "Return of the bergerbot :O",
               "I'm BAAAAAAAACKK!!!!!",
               "Ok, I'm back now.",
               "I read. Quite enjoying my newfound literacy.",
               "*yawn* How long was I asleep?"]
    
    if open("discord_log.txt").readlines()[-2].startswith("MANUAL"):
        client.send_message(botchannel, "RESTART\n\n"+random.choice(wakeups))
    else:
        print open("discord_log.txt").readlines()[-2]

@client.event
def on_message(message):
    if message.author.id != client.user.id and message.channel.name == 'bergerbot':
        print message.author.name+": "+message.content
        cmdHandle(client, message)
    
try:
    client.run()
except:
    with open('discord_log.txt', 'a') as log:
        log.write("\nCRASH "+time.strftime("%Y-%m-%d %H:%M:%S")+" after up for "+str(time.time()-inittime)+" seconds")
    raise
