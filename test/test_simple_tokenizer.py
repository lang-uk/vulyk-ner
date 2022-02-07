import time
import unittest

from bin.convert2vulyk import simple_tokenizer


class TestSimpleTokenizer(unittest.TestCase):
    def test_empty_tokenized(self):
        data = ""
        expected = []
        self.assertEqual(expected, list(simple_tokenizer(data)))

    def test_simple_tokenized(self):
        data = "Мама мила раму"
        expected = []
        self.assertEqual([["Мама", "мила", "раму"]], list(simple_tokenizer(data)))

    def test_sentences(self):
        data = "Мама мила раму !\nРама була біла ."
        expected = []
        self.assertEqual([["Мама", "мила", "раму", "!"], ["Рама", "була", "біла", "."]], list(simple_tokenizer(data)))


if __name__ == "__main__":
    unittest.main()
