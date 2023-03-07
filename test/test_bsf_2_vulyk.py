import time
import unittest

from bin.convert2vulyk import convert_bsf_2_vulyk, simple_tokenizer


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
T2 MISC 24 30 Другий"""
        expected = [["T1", "ORG", [(10, 15)]], ["T2", "MISC", [(23, 29)]]]
        result = convert_bsf_2_vulyk(data, bsf_markup, compensate_for_offsets=True)
        self.assertEqual(expected, result["entities"])
        self.assertEqual(self._get_sentences(result), ["Речення з Токен.", "токен Другий"])
        self.assertEqual(self._get_words(result), ["Речення", "з", "Токен", ".", "токен", "Другий"])
        self.assertEqual(self._get_entities(result), ["Токен", "Другий"])

    def test_entities_alignement(self):
        data: list[list[str]] = [["Семпл  ", "з", "Токен", "."], ["токен", "Другий"]]
        bsf_markup: str = """T1 ORG 10 15 Токен
T2 MISC 24 30 Другий"""
        expected = [["T1", "ORG", [(8, 13)]], ["T2", "MISC", [(21, 27)]]]
        result = convert_bsf_2_vulyk(data, bsf_markup, compensate_for_offsets=True)
        self.assertEqual(expected, result["entities"])
        self.assertEqual(self._get_sentences(result), ["Семпл з Токен.", "токен Другий"])
        self.assertEqual(self._get_words(result), ["Семпл", "з", "Токен", ".", "токен", "Другий"])
        self.assertEqual(self._get_entities(result), ["Токен", "Другий"])

    def test_complicated_realignment(self):
        data: list[list[str]] = simple_tokenizer(
            """Така любов до скрипки у Романа Шмігельського змалку , бо де б не збиралися в свята односельці , завжди була музика , пісня .
Тож співав усюди , а про музичний інструмент мріяв .
Хоч і професію сільському хлопцеві вдалося здобути потрібну , і робота слюсаря пошанована , але залюбки співав і в церковному хорі , і в художній самодіяльності .
Мабуть , за золоті руки й за чудовий тенор полюбила його пані Анна , з якою вони разом уже більш як півстоліття , і синів добрих виховали , які подарували їм онуків і правнука .

Саме народження первістка Олексія спонукало пана Романа опанувати музичну грамоту .
Але в той час вечірньої музичної школи не було , тож їздив до Калуша на приватні уроки , а згодом аж з Києва привіз бандуру .
"""
        )
        bsf_markup: str = """T1 LOC 666 672 Калуша
T2 LOC 707 712 Києва
"""
        expected = [["T1", "LOC", [(649, 655)]], ["T2", "LOC", [(689, 694)]]]
        result = convert_bsf_2_vulyk(data, bsf_markup, compensate_for_offsets=True)
        self.assertEqual(expected, result["entities"])
        self.assertEqual(self._get_entities(result), ["Калуша", "Києва"])

    def test_bug_no_1(self):
        data: list[list[str]] = simple_tokenizer("""А . де Барі розробив а П . Ідоров запровадив.""")
        bsf_markup: str = """T1 PERS 0 11 А . де Барі
T2 PERS 23 33 П. Ідоров"""
        expected = [["T1", "PERS", [(0, 10)]], ["T2", "PERS", [(22, 31)]]]
        result = convert_bsf_2_vulyk(data, bsf_markup, compensate_for_offsets=True)
        self.assertEqual(expected, result["entities"])
        self.assertEqual(self._get_entities(result), ["А. де Барі", "П. Ідоров"])

    def test_bug_no_2(self):
        data: list[list[str]] = simple_tokenizer(
            "Окремо ставиться тема , з’явлена в розлогому "
            "заголовку вірша : « Про тих багатих людей , що вступають із світових розкошей в убоге й нищотне "
            "іноче життя , щоб не жаліли й не каялися по тому , не призапастивши на свої пожитки маєтка , "
            "тобто речей , їжі та пиття . А передусім грошей , оскільки без маєтку в монастирях важко , особливо "
            "тим , що раніше мали багатство » ."
        )
        bsf_markup: str = (
            "T1 MISC 65 364 Про тих багатих людей, що вступають із світових розкошей в убоге й "
            "нищотне іноче життя, щоб не жаліли й не каялися по тому, не призапастивши на свої пожитки "
            "маєтка, тобто речей, їжі та пиття. А передусім грошей, оскільки без маєтку в монастирях важко, "
            "особливо тим, що раніше мали багатство"
        )

        expected = [["T1", "MISC", [(62, 352)]]]
        result = convert_bsf_2_vulyk(data, bsf_markup, compensate_for_offsets=True)
        self.assertEqual(expected, result["entities"])
        self.assertEqual(
            self._get_entities(result),
            [
                "Про тих багатих людей, що вступають із світових розкошей в убоге й "
                "нищотне іноче життя, щоб не жаліли й не каялися по тому, не призапастивши на свої пожитки "
                "маєтка, тобто речей, їжі та пиття. А передусім грошей, оскільки без маєтку в монастирях важко, "
                "особливо тим, що раніше мали багатство"
            ],
        )


if __name__ == "__main__":
    unittest.main()
