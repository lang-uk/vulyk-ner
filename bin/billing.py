# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import re
from codecs import open
from collections import Counter
import json
import sys

if __name__ == '__main__':
    if len(sys.argv) < 3:
        exit("Not enough arguments")

    counts = Counter()
    price = int(sys.argv[2]) / 100.
    with open(sys.argv[1], "r", encoding="utf-8") as f_in:
        for l in f_in:
            for answer in json.loads(l):

                word_count = 0
                for x in answer["answer"]["token_offsets"]:
                    word = answer["answer"]["text"][x[0]:x[1]]
                    if re.search(u"[а-яА-ЯєіїЄЇІ]", word) is not None:
                        word_count += 1

                counts[answer["user"]["username"]] += word_count

    for u, c in counts.most_common():
        print("%s: %s" % (u, c * price))
