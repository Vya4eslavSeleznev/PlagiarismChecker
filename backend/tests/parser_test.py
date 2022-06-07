import unittest
from unittest.mock import MagicMock

from file_parser import file_parser


class ParserTest(unittest.TestCase):

    def setUp(self):
        self.parser = file_parser.Parser()

    def test_get_data(self):
        file = 'file'

        self.parser.get_data = MagicMock()
        self.parser.get_data(file)
        self.parser.get_data.assert_called_once()
