import time
import unittest

from bin.convert2vulyk import reconstruct_tokenized


class TestReconstructTokenized(unittest.TestCase):
    def test_empty_tokenized(self):
        data = []
        expected = []
        self.assertEqual(expected, list(map(str, reconstruct_tokenized(data))))

    def test_simple_tokenized(self):
        data: list[list[str]] = [["Мама", "мила", "раму"]]
        self.assertEqual(["Мама", " ", "мила", " ", "раму"], list(map(str, reconstruct_tokenized(data))))

    def test_remove_spaces(self):
        data: list[list[str]] = [["Мама", " ", "мила", " ", "раму "]]
        self.assertEqual(["Мама", " ", "мила", " ", "раму"], list(map(str, reconstruct_tokenized(data))))

    def test_few_sentences(self):
        data: list[list[str]] = [["Мама", "мила", "раму", "!"], ["рама", "була", "біла", "?"]]
        self.assertEqual(
            ["Мама", " ", "мила", " ", "раму", "!", "\n", "рама", " ", "була", " ", "біла", "?"],
            list(map(str, reconstruct_tokenized(data))),
        )

    def test_punctuation(self):
        data: list[list[str]] = [["Мамо", ",", "навіщо", "!", "?"], ["Адже", ",", "рама", "була", "біла", "."]]
        self.assertEqual(
            ["Мамо", ",", " ", "навіщо", "!", "?", "\n", "Адже", ",", " ", "рама", " ", "була", " ", "біла", "."],
            list(map(str, reconstruct_tokenized(data))),
        )

    def test_quotes(self):
        data: list[list[str]] = [
            ["Тендер", "“", "виграв", "”", "ТОВ", "«", "ЛАБЄАН-хісв", "»", "."],
            ["Сумна", "історія", ",", "малята", "."],
        ]
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
            list(map(str, reconstruct_tokenized(data))),
        )

    def test_brackets(self):
        data: list[list[str]] = [
            ["Ой", "лишенько", "(", "[", "скільки", "ж", "тут", "дужок", "]", ")", ",", "це", "що", ",", "лісп", "?"],
        ]

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
            list(map(str, reconstruct_tokenized(data))),
        )

    def _get_words(self, text: str, tokens: list[tuple[int, int]]) -> list[str]:
        return [text[i1:i2] for (i1, i2) in tokens]

    def test_spaces_alignement(self):
        data: list[list[str]] = [
            ["Цікаве", " ", "питання"],
        ]

        adjusted_tokens: list[AlignedToken] = list(reconstruct_tokenized(data))
        adjusted_text: str = "".join((map(str, adjusted_tokens)))
        whitespaced_text: str = "\n".join(" ".join(sent) for sent in data)

        self.assertEqual(
            "Цікаве питання",
            adjusted_text,
        )

        self.assertEqual(
            [
                "Цікаве",
                " ",
                "питання",
            ],
            self._get_words(adjusted_text, [t.new_pos for t in adjusted_tokens]),
        )

        self.assertEqual(
            [
                "Цікаве",
                " ",
                "питання",
            ],
            self._get_words(whitespaced_text, [t.orig_pos for t in adjusted_tokens]),
        )

    def test_simple_alignement(self):
        data: list[list[str]] = [
            ["Цікаве", "питання ", " , ", " Мурзіку", "."],
        ]

        adjusted_tokens: list[AlignedToken] = list(reconstruct_tokenized(data))
        adjusted_text: str = "".join((map(str, adjusted_tokens)))
        whitespaced_text: str = "\n".join(" ".join(sent) for sent in data)

        self.assertEqual(
            "Цікаве питання, Мурзіку.",
            adjusted_text,
        )

        self.assertEqual(
            [
                "Цікаве",
                " ",
                "питання",
                ",",
                " ",
                "Мурзіку",
                ".",
            ],
            self._get_words(adjusted_text, [t.new_pos for t in adjusted_tokens]),
        )

        self.assertEqual(
            [
                "Цікаве",
                " ",
                "питання ",
                " , ",
                " ",
                " Мурзіку",
                ".",
            ],
            self._get_words(whitespaced_text, [t.orig_pos for t in adjusted_tokens]),
        )

    def test_hanging_spaces_alignement(self):
        data: list[list[str]] = [
            [" ", " Цікаве ", "питання ", " , ", " Мурзіку", "."],
        ]

        adjusted_tokens: list[AlignedToken] = list(reconstruct_tokenized(data))
        adjusted_text: str = "".join((map(str, adjusted_tokens)))
        whitespaced_text: str = "\n".join(" ".join(sent) for sent in data)

        self.assertEqual(
            "Цікаве питання, Мурзіку.",
            adjusted_text,
        )

        self.assertEqual(
            [
                "Цікаве",
                " ",
                "питання",
                ",",
                " ",
                "Мурзіку",
                ".",
            ],
            self._get_words(adjusted_text, [t.new_pos for t in adjusted_tokens]),
        )

        self.assertEqual(
            [
                " Цікаве ",
                " ",
                "питання ",
                " , ",
                " ",
                " Мурзіку",
                ".",
            ],
            self._get_words(whitespaced_text, [t.orig_pos for t in adjusted_tokens]),
        )

    def test_alignement(self):
        data: list[list[str]] = [
            ["Цікаве", "питання", ", ", " ", "Мурзіку", "   ", "Васильовичу", "."],
            ["Будемо", " ", "полемізувати", " ."],
        ]

        adjusted_tokens: list[AlignedToken] = list(reconstruct_tokenized(data))
        adjusted_text: str = "".join((map(str, adjusted_tokens)))
        whitespaced_text: str = "\n".join(" ".join(sent) for sent in data)

        self.assertEqual(
            "Цікаве питання, Мурзіку Васильовичу.\nБудемо полемізувати.",
            adjusted_text,
        )

        self.assertEqual(
            [
                "Цікаве",
                " ",
                "питання",
                ",",
                " ",
                "Мурзіку",
                " ",
                "Васильовичу",
                ".",
                "\n",
                "Будемо",
                " ",
                "полемізувати",
                ".",
            ],

            self._get_words(adjusted_text, [t.new_pos for t in adjusted_tokens]),
        )

        self.assertEqual(
            self._get_words(whitespaced_text, [t.orig_pos for t in adjusted_tokens]),
            [
                "Цікаве",
                " ",
                "питання",
                ", ",
                " ",
                "Мурзіку",
                " ",
                "Васильовичу",
                ".",
                "\n",
                "Будемо",
                " ",
                "полемізувати",
                " .",
            ],
        )

    def test_alignement_cornercase1(self):
        data: list[list[str]] = [["Семпл  ", "з", "Токен", "."], ["токен", "Другий"]]

        adjusted_tokens: list[AlignedToken] = list(reconstruct_tokenized(data))
        adjusted_text: str = "".join((map(str, adjusted_tokens)))
        whitespaced_text: str = "\n".join(" ".join(sent) for sent in data)

        self.assertEqual(
            "Семпл з Токен.\nтокен Другий",
            adjusted_text,
        )

        self.assertEqual(
            [
                "Семпл",
                " ",
                "з",
                " ",
                "Токен",
                ".",
                "\n",
                "токен",
                " ",
                "Другий",
            ],

            self._get_words(adjusted_text, [t.new_pos for t in adjusted_tokens]),
        )

        self.assertEqual(
            self._get_words(whitespaced_text, [t.orig_pos for t in adjusted_tokens]),
            [
                "Семпл  ",
                " ",
                "з",
                " ",
                "Токен",
                ".",
                "\n",
                "токен",
                " ",
                "Другий",
            ],
        )


if __name__ == "__main__":
    unittest.main()
