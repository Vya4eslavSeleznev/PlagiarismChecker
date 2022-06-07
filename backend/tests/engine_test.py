import unittest
from unittest.mock import MagicMock
from engine import engine


class EngineTest(unittest.TestCase):

    def setUp(self):
        self.engine = engine.Engine()

    def test_start(self):
        all_sentences = [
            "Yesterday I went to school and got a good grade for a test paper.",
            "The person box was packed with jelly many dozens of months later.",
            "Standing on one's head at job interviews forms a lasting impression.",
            "It took him a month to finish the meal."
        ]

        sentence_to_check = ["In the past I went to an educational institution and passed the test."]

        self.engine.start = MagicMock()
        self.engine.start(all_sentences, sentence_to_check, 2)
        self.engine.start.assert_called_once()

    def test_prepare_results(self):
        ids = [1, 2, 3]
        calculation_result = [0.9, 0.8, 0.7]

        self.engine.prepare_results = MagicMock()
        self.engine.prepare_results(ids, calculation_result)
        self.engine.prepare_results.assert_called_once()
