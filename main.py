import xml.etree.ElementTree as ET
tree = ET.parse('Text.xml')
root = tree.getroot()

class NPC:
    """
           Parameters
           ----------
           name : str
               Name of the character
           num : str
               Starting dialogue branch
    """
    name = "John"
    num = "001"


def game():
    """Primary game while loop"""
    npc = NPC
    while True:
        talk(npc)
        break

def talk(npc):
    """Conversation while loop (will be)"""
    getDialogue(npc, None)
    while True:
        response = input()
        finished = getDialogue(npc, response)
        if finished == 0:
            break;

def getDialogue(npc, response):
    """XML parser.

            iterates through XML comversation tree to extract the correct dialogue. 'line' is the desired xml tag,
            this nested structure can be searched through for the correct responses.

            Parameters
            ----------
            npc : object, neccessary
                the person the hero is speaking to
            response : str, optional
                the user input (default is None)
    """
    for branch in root.iter('data'):
        for line in branch:
            if line.get("id") == npc.num:
                if None == response:
                    # get initial speech
                    for message in line.iter('message'):
                        print(npc.name + ": " + message.text)
                    i = 0
                    for choice in line.iter('command'):
                        print(str(i) + ": " + choice.text)
                        i += 1
                else:
                    # options after user input
                    for result in line.iter('choice'):
                        if result.get("id") == response:
                            for output in result.iter('result'):
                                print(output.text)
                                return 0

if __name__ == '__main__':
    game()

