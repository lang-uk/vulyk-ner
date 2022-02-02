import time
import unittest

from bin.convert2vulyk import convert_bsf_2_vulyk, reconstruct_tokenized


class TestBsf2Vulyk(unittest.TestCase):
    def setUp(self) -> None:
        self.vulyk_base = {
            "modifications": [],
            "equivs": [],
            "protocol": 1,
            "ctime": int(time.time()),
            "triggers": [],
            "text": "",
            "source_files": ["ann", "txt"],
            "messages": [],
            "sentence_offsets": [],
            "comments": [],
            "entities": [],
            "mtime": int(time.time()),
            "relations": [],
            "token_offsets": [],
            "action": "getDocument",
            "normalizations": [],
            "attributes": [],
            "events": [],
            "document": "",
            "collection": "/",
        }

    def _get_sentences(self, result: dict) -> list[str]:
        return [result["text"][i1:i2] for (i1, i2) in result["sentence_offsets"]]

    def _get_words(self, result: dict) -> list[str]:
        return [result["text"][i1:i2] for (i1, i2) in result["token_offsets"]]

    def _get_entities(self, result: dict) -> list[str]:
        res: list[str] = []

        for _, _, ent in result["entities"]:
            for i1, i2 in ent:
                res.append(result["text"][i1:i2])

        return res

    def test_empty_vulyk(self):
        data: list = []
        bsf_markup: str = ""
        expected = self.vulyk_base
        self.assertEqual(expected, convert_bsf_2_vulyk(data, bsf_markup))

    def test_no_ents(self):
        data: list[list[str]] = [["Текст", "без", "сутностей"]]
        bsf_markup = ""

        result: dict = convert_bsf_2_vulyk(data, bsf_markup)

        self.assertEqual(result["text"], "Текст без сутностей")

        self.assertEqual([], result["entities"])

        self.assertEqual(self._get_sentences(result), ["Текст без сутностей"])

        self.assertEqual(self._get_words(result), ["Текст", "без", "сутностей"])

        self.assertEqual([(0, 19)], result["sentence_offsets"])

    def test_tok_idx(self):
        data: list[list[str]] = [["розпорядження", "землями", "\n", "в", "межах", ",", "визначених"]]

        bsf_markup: str = ""
        tok_idx: list[tuple[int, int]] = [(0, 13), (14, 21), (22, 23), (24, 29), (29, 30), (31, 41)]

        result: dict = convert_bsf_2_vulyk(data, bsf_markup)
        self.assertEqual(tok_idx, result["token_offsets"])

        self.assertEqual(self._get_words(result), ["розпорядження", "землями", "в", "межах", ",", "визначених"])

        self.assertEqual(self._get_sentences(result), ["розпорядження землями в межах, визначених"])

        self.assertEqual(result["text"], "розпорядження землями в межах, визначених")

    def test_sentence_offset(self):
        data: list[list[str]] = [["Речення", "номер", "1", "."], ["Рядок", "другий"]]

        bsf_markup: str = ""
        sent_idx: list[tuple[int, int]] = [(0, 16), (17, 29)]
        result: dict = convert_bsf_2_vulyk(data, bsf_markup)
        self.assertEqual(sent_idx, result["sentence_offsets"])
        self.assertEqual([], result["entities"])
        self.assertEqual(self._get_sentences(result), ["Речення номер 1.", "Рядок другий"])
        self.assertEqual(self._get_words(result), ["Речення", "номер", "1", ".", "Рядок", "другий"])

    def test_entities_offset(self):
        data: list[list[str]] = [["Речення", "з", "Токен", "."], ["токен", "Другий"]]
        bsf_markup: str = """T1 ORG 10 15 Токен
T2 MISC 23 31 Другий"""
        expected = [["T1", "ОРГ", [(10, 15)]], ["T2", "РІЗН", [(23, 31)]]]
        result = convert_bsf_2_vulyk(data, bsf_markup)
        self.assertEqual(expected, result["entities"])
        self.assertEqual(self._get_sentences(result), ["Речення з Токен.", "токен Другий"])
        self.assertEqual(self._get_words(result), ["Речення", "з", "Токен", ".", "токен", "Другий"])
        self.assertEqual(self._get_entities(result), ["Токен", "Другий"])


if __name__ == "__main__":
    unittest.main()
