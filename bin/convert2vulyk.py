#!env python

import argparse
import json
import logging
import re
import sys
import time
from collections import namedtuple

log = logging.getLogger(__name__)
log.setLevel(logging.ERROR)

BsfInfo = namedtuple('BsfInfo', 'id, tag, start_idx, end_idx, token')


def parse_bsf(bsf_data: str) -> list:
    """
    Convert multiline textual bsf representation to a list of named entities.

    :param bsf_data: data in the format 'T9	PERS 778 783    токен'. Can be multiple lines.
    :return: list of named tuples for each line of the data representing a single named entity token
    """
    data = bsf_data.strip()
    if not data:
        return []
    #                     Token_id Entity start  end    text within range
    #                        \/      \/     \/    \/      \/
    ln_ptrn = re.compile(r'(T\d+)\s(\w+)\s(\d+)\s(\d+)\s(.+?)(?=T\d+\s\w+\s\d+\s\d+|$)', flags=re.DOTALL)
    result = []
    for m in ln_ptrn.finditer(data):
        bsf = BsfInfo(m.group(1), m.group(2), int(m.group(3)), int(m.group(4)), m.group(5).strip())
        result.append(bsf)
    return result


def convert_bsf_2_vulyk(text: str, bsf_markup: str) -> dict:
    """
    Given tokenized text and named entities in Brat standoff format, generate object
    in the format compatible with Vulyk markup tool.
    :param text: tokenized text (space as separator)
    :param bsf_markup: named entities in Brat standoff format
    :return: dict that can be directly converted to Vulyk json file
    """
    bsf = parse_bsf(bsf_markup)
    ents = [[e.id, e.tag, [[e.start_idx, e.end_idx]]] for e in bsf]

    idx = 0
    t_idx = 0
    s_offsets = []
    t_offsets = []
    if text:
        for s in text.split('\n'):
            s_offsets.append([idx, idx + len(s)])
            for t in s.strip().split(' '):
                t_offsets.append([t_idx, t_idx + len(t)])
                t_idx += len(t) + 1

            idx += len(s) + 1
            t_idx = idx

    ts = int(time.time())
    vulyk = {"modifications": [], "equivs": [], "protocol": 1, "ctime": ts, "triggers": [], "text": text,
              "source_files": ["ann", "txt"], "messages": [], "sentence_offsets": s_offsets, "comments": [],
              "entities": ents, "mtime": ts, "relations": [], "token_offsets": t_offsets, "action": "getDocument",
              "normalizations": [], "attributes": [], "events": [], "document": "", "collection": "/"}

    return vulyk


def text_2_vulyk(text: str, bsf_markup: str = None) -> str:
    """
    Convert text string with annotations to json string for Vulyk annotation tool.
    If annotations are provided in bsf_markup then text must be tokenized. Otherwise a raw text string can be supplied.
    :param text: tokenzied OR raw text string
    :param bsf_markup: string containing annotations in brat standoff format
    :return: json string compatible with Vulyk (Brat annotation tool)
    """
    txt = text
    markup = bsf_markup
    if bsf_markup is None:
        log.info("No markup file => processing text with Stanza to extract Named Entities.")
        # run tokenization and NER
        from tokenize_uk import tokenize_text
        token_list = tokenize_text(text)
        # we have list<paragraphs> of list<sentences> of list<tokens>
        paragraph = ['\n'.join([' '.join(t) for t in sent]) for sent in token_list]
        txt = '\n'.join(paragraph)  # stanza bug does not allow for double new line symbol right now
        log.debug(txt)

        markup = _run_ner(txt)
        log.debug(markup)

    vulyk_obj = convert_bsf_2_vulyk(txt, markup)

    return json.dumps(vulyk_obj, ensure_ascii=False)


def _run_ner(txt: str) -> str:
    """
    Run ner pipeline on tokenized text using Stanza.
    :param txt: tokenized text string
    :return: string with annotations in brat standoff format
    """
    import stanza
    logging.getLogger("stanza").setLevel(log.level)

    stanza.download('uk')

    ner = stanza.Pipeline(lang='uk', processors='tokenize,mwt,ner', tokenize_pretokenized='true')
    log.info("Processing text. It may take few seconds...")
    doc = ner(txt)

    tok_i = 1
    brat_str = ""
    for ent in doc.ents:
        brat_str += f'T{tok_i}\t{ent.type} {ent.start_char} {ent.end_char}\t{ent.text}\n'
        tok_i += 1
    return brat_str


if __name__ == "__main__":
    logging.basicConfig()

    parser = argparse.ArgumentParser(
        description='Convert text (tokenized or generic) to json file supported by Vulyk. '
                    'Data file can be supplied via cmd line arguments '
                    'or you can pipe data in and out of this script like:'
                    '`cat file.txt | python3 convert2vulyk.py > save_to_file.json`')
    parser.add_argument('text_file', nargs="?", type=argparse.FileType('r'), default=sys.stdin,
                        help='Text file to process. If file path not provided, assumes stdin stream.'
                             ' Must be tokenized if --brat_file is provided. '
                             '*.ann for lang-uk data set')
    parser.add_argument('--brat_annotation', type=argparse.FileType('r'), default=None,
                        help='Path to file with Brat standoff markup')
    parser.add_argument('-v', action='store_true', help='Print more logs (info)')
    parser.add_argument('-vv', action='store_true', help='Print even more logs (debug)')

    args = parser.parse_args()

    if args.vv:
        log.setLevel(logging.DEBUG)
    elif args.v:
        log.setLevel(logging.INFO)

    brat_markup = None
    if args.brat_annotation is not None:  # read markup
        log.info(f"Reading markup from file")
        brat_markup = args.brat_annotation.read()
        log.debug(brat_markup)
    else:
        log.info(f"No markup file is provided. Assuming a raw text as input.")

    text_data = args.text_file.read()

    vulyk_json = text_2_vulyk(text_data, brat_markup)
    print(vulyk_json)
