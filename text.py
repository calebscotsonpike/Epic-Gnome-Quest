import xml.etree.ElementTree as ET

class Text():

    def __init__(self, game):
        self.game = game
        self.tree = ET.parse('Text.xml')
        self.root = self.tree.getroot()


    def talk(self, npc):
        """Conversation while loop (will be)"""

        self.name = npc.name
        self.num = npc.dialogue_num
        while True:
            self.conversation(self.name, self.num, None)
            response = input()
            if response in ['0', '1']:
                self.num = self.conversation(self.name, self.num, response)
            else:
                self.game.draw_text('INVALID' + '\n')
                self.game.update()
            if self.num == '0':
                break

    def conversation(self, name, num, response):
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
        for branch in self.root.iter('data'):
            for dialogue in branch:
                if dialogue.get("id") == num:
                    if None == response:
                        # get initial speech
                        for message in dialogue.iter('message'):
                            self.game.draw_text(name + ": " + message.text + '\n')
                            self.game.update()
                        i = 0
                        for choice in dialogue.iter('command'):
                            self.game.draw_text(str(i) + ": " + choice.text + '\n')
                            self.game.update()
                            i += 1
                    else:
                        # options after user input
                        for choice in dialogue.iter('choice'):
                            if choice.get("id") == response:
                                for result in choice.iter('result'):
                                    if result.text is not None:
                                        self.game.draw_text(result.text + '\n')
                                        self.game.update()
                                    num = result.get("id")
                                    return num