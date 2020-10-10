import unittest

import text


class TestText(unittest.TestCase):
    def test_talk(self):
        """
        Test a talk method
        """
        t = text()
        self.assertEqual(self, t.talk('john', '001', '0'), '002')


if __name__ == '__main__':
    unittest.main()
