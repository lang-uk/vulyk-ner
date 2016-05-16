# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from codecs import open
from copy import deepcopy
from datetime import datetime
import json
import os
import re
import sys

from glob2 import glob

TEMPLATE = {
    "action": "getDocument",
    "attributes": [],
    "comments": [],
    "ctime": 1452432571.0,
    "mtime": 1452432571.0,
    "entities": [],
    "equivs": [],
    "events": [],
    "messages": [],
    "modifications": [],
    "normalizations": [],
    "protocol": 1,
    "relations": [],
    "sentence_offsets": [

    ],
    "source_files": [
        "ann",
        "txt"
    ],
    "text": "",
    "token_offsets": [
    ],
    "triggers": []
}


def parse_file(fname, content):
    matches = re.findall("<S>(.*)<\/S>", content)

    text = []
    words = []
    sentences = []

    word_count = 0
    token_begin = 0
    sentence_begin = 0
    res = deepcopy(TEMPLATE)

    for m in matches:
        word_forms = re.findall("([^[]*)\[([^]]*)\]", m)

        sentence_begin = len("".join(text))
        for word, _ in word_forms:
            leading_space = len(word) - len(word.lstrip(" "))
            trailing_space = len(word) - len(word.rstrip(" "))
            word = word.strip()

            text.append(" " * leading_space)

            token_begin = len("".join(text))
            text.append(word)
            if word and re.search(u"[а-яА-ЯєіїЄЇІ]", word) is not None:
                word_count += 1
            token_end = len("".join(text))

            text.append(" " * trailing_space)

            if token_end > token_begin:
                words.append([token_begin, token_end])

        text.append("\n")
        sentence_end = len("".join(text))
        if sentence_end > sentence_begin:
            sentences.append([sentence_begin, sentence_end])

    res["text"] = "".join(text)
    res["file_id"] = fname
    res["token_offsets"] = words
    res["sentence_offsets"] = sentences

    res["ctime"] = float(datetime.now().strftime("%s"))
    res["mtime"] = float(datetime.now().strftime("%s"))

    print("%s:%s" % (fname, word_count))
    return res


if __name__ == '__main__':
    if len(sys.argv) < 3:
        exit("Not enough arguments")

    with open(sys.argv[2], "w", encoding="utf-8") as f_out:
        for f in glob(sys.argv[1]):
            with open(f, "r", encoding="utf-8") as fp:
                f_out.write(
                    json.dumps(
                        parse_file(os.path.basename(f), fp.read()),
                        ensure_ascii=False) +
                    "\n")
