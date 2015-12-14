#Used to generate the database. If you have cloned entire repo, this file is not necessary, as a database is included.
import chatterbot
import parse_shakespeare

def train_bot(bot, plays=["j_caesar"]):
    dialogue = parse_shakespeare.getDialogueList(*plays)
    print "Training bot based on the text of "+" and ".join(["./shakespeare/"+p+".xml" for p in plays])+"...",
    for play in dialogue:
        for scene in play:
            bot.train(scene)
    print "Done!"
if __name__ == "__main__":
    bot = chatterbot.ChatBot("Julius Caesar", storage_adapter="chatterbot.adapters.storage.JsonDatabaseAdapter", database="julius_caesar.db")
    train_bot(bot)
    bot.storage.read_only=True
    
    import time
    
    while 1:
        query = raw_input(">")
        a = time.time()
        bot.get_response(query)
        print time.time() - a
