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
        y = 0
        dialogue_num = self.conversation(npc_name, dialogue_num, response, y)
        return dialogue_num

    def conversation(self, name, dialogue_num, response, y):
        """XML parser.

                iterates through XML conversation tree to extract the correct dialogue. 'dialogue' is the desired xml tag,
                this nested structure can be searched through for the correct responses.

                Parameters
                ----------
                name : NPC name
                dialogue_num : object, necessary
                    the person the hero is speaking to
                response : str, optional
                    the user input (default is None)

                Return
                ------
                dialogue_num : conversation branch number e.g. 001 or 0 to end interaction

        """
        for branch in self.root.iter('data'):
            for dialogue in branch:
                if dialogue.get("id") == dialogue_num:
                    if response is None:
                        # get initial speech
                        for message in dialogue.iter('message'):
                            self.game.onscreen_text.append(((0, y), name + ": " + message.text))
                            if message.get('id') is not None:
                                dialogue_num = message.get('id')
                            y += 32
                        i = 0
                        for choice in dialogue.iter('command'):
                            self.game.onscreen_text.append(((0, y), str(i) + ": " + choice.text))
                            y += 32
                            i += 1
                        return dialogue_num
                    else:
                        # options after user input
                        for choice in dialogue.iter('choice'):
                            if choice.get("id") == response:
                                for result in choice.iter('result'):
                                    if result.text is not None:
                                        self.game.onscreen_text.append(((0, y), result.text))
                                        y += 32
                                    dialogue_num = result.get("id")
                                    return dialogue_num
