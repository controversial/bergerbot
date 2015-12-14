from main import reply_generator
from shakespeare import shakespeare

def genReply(message, userRoles, channelname):
    channelname = str(channelname)
    if channelname == "bergerbot":
        print 'bergerbot'
        return reply_generator.processMsg(message, userRoles)
    elif channelname == "shakespeare":
        print 'shakespeare'
        return [["SAY",shakespeare.get_shakespeare_response(message)]]
    elif channelname == "general":
        print 'general'
        return [["DEL"]]
