#This file is for the purpose of retrieving dialog from a shakespeare XML file to make it easy to train a chatterbot. 
import xml.etree.ElementTree as ET
import os

def absolute(path):
    return os.path.join(os.path.dirname(os.path.abspath(__file__)),path)

def getDialogueList(*plays):
    dialogues = []
    for p in plays:
        root = ET.parse(absolute("shakespeare/"+p+".xml"))

        playtitle = root.findtext("TITLE")
        playsubt = root.findtext("PLAYSUBT")
        print playtitle

        dialogue_by_scene = []

        acts = root.findall("ACT")
        for act in acts:
            print "    "+act.findtext("TITLE")
            scenes = act.findall("SCENE")
            for scene in scenes:
                print "        "+scene.findtext("TITLE")
                speeches = scene.findall("SPEECH")
                dialogue = ["\n".join([s.text for s in speech.findall("LINE") if s.text]) for speech in speeches]
                dialogue_by_scene.append(dialogue)
        dialogues.append(dialogue_by_scene)
        print "\n\n"
    return dialogues

if __name__ == "__main__":
    print getDialogueList("j_caesar", "hamlet")
