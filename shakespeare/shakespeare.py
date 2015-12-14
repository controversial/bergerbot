import os

def absolute(path):
    return os.path.join(os.path.dirname(os.path.abspath(__file__)),path)

from chatterbot import ChatBot
caesar = ChatBot("Julius Caesar",
                 storage_adapter="chatterbot.adapters.storage.MongoDatabaseAdapter",                            
                 database="julius_caesar")

if len(caesar.storage.filter()) == 0:
    import train
    train.train_bot(caesar)

caesar.storage.read_only = True
    
def get_shakespeare_response(inp):
    return caesar.get_response(inp)

if __name__ == "__main__":
    import time
    while 1:
        inp=raw_input("> ")
        a=time.time()
        get_shakespeare_response(inp)
        print time.time()-a
