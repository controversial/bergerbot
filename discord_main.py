import discord
import random
import time
import traceback
import os

from reply_generator import genReply

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
    cmds = genReply(message.content, userRoles, message.channel.name)
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

@client.event
def on_message(message):
    if message.author.id != client.user.id:
        print message.author.name+": "+message.content
        cmdHandle(client, message)
    
try:
    client.run()
except:
    with open('discord_log.txt', 'a') as log:
        log.write("\nCRASH "+time.strftime("%Y-%m-%d %H:%M:%S")+" after up for "+str(time.time()-inittime)+" seconds")
    raise
