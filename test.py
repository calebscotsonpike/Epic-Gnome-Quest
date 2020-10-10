import unittest

from text import Text
from game import Game


class TestText(unittest.TestCase):

    def test_talk(self):
        """
        Test a talk method
        """
        game = Game()
        text = Text(game)
        self.assertEqual(self, text.talk('john', '001', '0'), '002')


if __name__ == '__main__':
    unittest.main()
