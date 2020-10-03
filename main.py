import xml.etree.ElementTree as ET
tree = ET.parse('Text.xml')
root = tree.getroot()

class NPC:
    name = "John"

def game():
    npc = NPC
    while True:
        talk("001", npc)
        break

def talk(num, npc):
    getDialogue(num, npc, None)
    response = input()
    getDialogue(num,npc, response)

def getDialogue(num, npc, response):
    if None == response:
        for branch in root.iter('data'):
            for tag in branch:
                if tag.get("id") == num:
                    for message in tag.iter('message'):
                        print(npc.name + ": " + message.text)
                    i = 0
                    for choice in tag.iter('command'):
                        print(str(i) + ": " + choice.text)
                        i += 1
    else:
        print("")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    game()

