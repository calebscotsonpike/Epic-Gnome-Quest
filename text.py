import xml.etree.ElementTree as ET

class Text():

    def __init__(self, game):
        self.game = game
        self.tree = ET.parse('Text.xml')
        self.root = self.tree.getroot()

    def talk(self, npc_name, dialogue_num, response):
        """Conversation while loop (will be)"""
        if response == '':
            response = None
        line = 0
        dialogue_num = self.conversation(npc_name, dialogue_num, response, line)
        if response in ['0', '1']:
            dialogue_num = self.conversation(npc_name, dialogue_num, None, line)
            dialogue_num = self.conversation(npc_name, dialogue_num, response, line)
            self.conversation(npc_name, dialogue_num, response, line)
        if dialogue_num == '0':
            return True


        #if response in ['']:
        #    return num
        #else:
        #    self.game.draw_text('INVALID', (line+25))
        #if num == '0':
        #    return True

    def conversation(self, name, num, response, line):
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

                Return
                ------
                num : conversation branch number e.g. 001 or 0 to end interaction

        """
        for branch in self.root.iter('data'):
            for dialogue in branch:
                if dialogue.get("id") == num:
                    if response is None:
                        # get initial speech
                        for message in dialogue.iter('message'):
                            self.game.draw_text(name + ": " + message.text, line)
                            line += 25
                        i = 0
                        for choice in dialogue.iter('command'):
                            self.game.draw_text(str(i) + ": " + choice.text, line)
                            line += 25
                            i += 1
                    else:
                        # options after user input
                        for choice in dialogue.iter('choice'):
                            if choice.get("id") == response:
                                for result in choice.iter('result'):
                                    if result.text is not None:
                                        self.game.draw_text(result.text, line)
                                        line += 25
                                    num = result.get("id")
                                    return num