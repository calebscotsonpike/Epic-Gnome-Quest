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
    name = npc.name
    num = npc.num
    while True:
        conversation(name, num, None)
        response = input()
        if response in ['0','1']:
            num = conversation(name, num, response)
        else:
            print('INVALID')
        if num == '0':
            break


def conversation(name, num, response):
    """XML parser.

            iterates through XML conversation tree to extract the correct dialogue. 'dialogue' is the desired xml tag,
            this nested structure can be searched through for the correct responses.

            Parameters
            ----------
            name : NPC name
            num : object, necessary
                the person the hero is speaking to
            response : str, optional
                the user input (default is None)
    """
    for branch in root.iter('data'):
        for dialogue in branch:
            if dialogue.get("id") == num:
                if None == response:
                    # get initial speech
                    for message in dialogue.iter('message'):
                        print(name + ": " + message.text)
                    i = 0
                    for choice in dialogue.iter('command'):
                        print(str(i) + ": " + choice.text)
                        i += 1
                else:
                    # options after user input
                    for choice in dialogue.iter('choice'):
                        if choice.get("id") == response:
                            for result in choice.iter('result'):
                                if result.text != None:
                                    print(result.text)
                                num = result.get("id")
                                return num


if __name__ == '__main__':
    game()
