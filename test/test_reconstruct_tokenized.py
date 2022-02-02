import time
import unittest

from bin.convert2vulyk import reconstruct_tokenized


class TestReconstructTokenized(unittest.TestCase):
    def test_empty_tokenized(self):
        data = []
        expected = []
        self.assertEqual(expected, list(reconstruct_tokenized(data)))

    def test_simple_tokenized(self):
        data = [["Мама", "мила", "раму"]]
        expected = []
        self.assertEqual(["Мама", " ", "мила", " ", "раму"], list(reconstruct_tokenized(data)))

    def test_remove_spaces(self):
        data = [["Мама", " ", "мила", " ", "раму "]]
        expected = []
        self.assertEqual(["Мама", " ", "мила", " ", "раму"], list(reconstruct_tokenized(data)))

    def test_few_sentences(self):
        data = [["Мама", "мила", "раму", "!"], ["рама", "була", "біла", "?"]]
        expected = []
        self.assertEqual(
            ["Мама", " ", "мила", " ", "раму", "!", "\n", "рама", " ", "була", " ", "біла", "?"],
            list(reconstruct_tokenized(data)),
        )

    def test_punctuation(self):
        data = [["Мамо", ",", "навіщо", "!", "?"], ["Адже", ",", "рама", "була", "біла", "."]]
        expected = []
        self.assertEqual(
            ["Мамо", ",", " ", "навіщо", "!", "?", "\n", "Адже", ",", " ", "рама", " ", "була", " ", "біла", "."],
            list(reconstruct_tokenized(data)),
        )

    def test_quotes(self):
        data = [
            ["Тендер", "“", "виграв", "”", "ТОВ", "«", "ЛАБЄАН-хісв", "»", "."],
            ["Сумна", "історія", ",", "малята", "."],
        ]
        expected = []
        self.assertEqual(
            [
                "Тендер",
                " ",
                "“",
                "виграв",
                "”",
                " ",
                "ТОВ",
                " ",
                "«",
                "ЛАБЄАН-хісв",
                "»",
                ".",
                "\n",
                "Сумна",
                " ",
                "історія",
                ",",
                " ",
                "малята",
                ".",
            ],
            list(reconstruct_tokenized(data)),
        )

    def test_brackets(self):
        data = [
            ["Ой", "лишенько", "(", "[", "скільки", "ж", "тут", "дужок", "]", ")", ",", "це", "що", ",", "лісп", "?"],
        ]
        expected = []
        self.assertEqual(
            [
                "Ой",
                " ",
                "лишенько",
                " ",
                "(",
                "[",
                "скільки",
                " ",
                "ж",
                " ",
                "тут",
                " ",
                "дужок",
                "]",
                ")",
                ",",
                " ",
                "це",
                " ",
                "що",
                ",",
                " ",
                "лісп",
                "?",
            ],
            list(reconstruct_tokenized(data)),
        )


if __name__ == "__main__":
    unittest.main()
