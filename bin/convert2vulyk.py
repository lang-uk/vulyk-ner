#!env python

import argparse
import json
import logging
import re
import sys
import time
import glob
import pathlib
from tokenize_uk import tokenize_text
from collections import namedtuple

log = logging.getLogger(__name__)

BsfInfo = namedtuple("BsfInfo", "id, tag, start_idx, end_idx, token")


class StanzaNER:
    def __init__(self, model):
        import stanza

        logging.getLogger("stanza").setLevel(log.level)
        stanza.download(model)

        self.ner = stanza.Pipeline(lang=model, processors="tokenize,mwt,ner", tokenize_pretokenized="true")

    def tag_text(self, txt):
        doc = self.ner(txt)

        tok_i = 1
        brat_str = ""

        for tok_i, ent in enumerate(doc.ents):
            brat_str += f"T{tok_i + 1}\t{ent.type} {ent.start_char} {ent.end_char}\t{ent.text}\n"

        return brat_str


class SpacyNER:
    def __init__(self, model):
        import spacy

        self.ner = spacy.load(model)

    def tag_text(self, txt):
        doc = self.ner(txt)

        brat_str = ""

        if doc.ents:
            for tok_i, ent in enumerate(doc.ents):
                brat_str += f"T{tok_i + 1}\t{ent.label_} {ent.start_char} {ent.end_char}\t{ent.text}\n"

        return brat_str


def parse_bsf(bsf_data: str) -> list:
    """
    Convert multiline textual bsf representation to a list of named entities.

    :param bsf_data: data in the format 'T9 PERS 778 783    токен'. Can be multiple lines.
    :return: list of named tuples for each line of the data representing a single named entity token
    """

    data = bsf_data.strip()
    if not data:
        return []
    #                     Token_id Entity start  end    text within range
    #                        \/      \/     \/    \/      \/
    ln_ptrn = re.compile(r"(T\d+)\s(\w+)\s(\d+)\s(\d+)\s(.+?)(?=T\d+\s\w+\s\d+\s\d+|$)", flags=re.DOTALL)
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

    tags_mapping = {"PERS": "ПЕРС", "ORG": "ОРГ", "LOC": "ЛОК", "MISC": "РІЗН"}

    bsf = parse_bsf(bsf_markup)
    ents = [[e.id, tags_mapping.get(e.tag, e.tag), [[e.start_idx, e.end_idx]]] for e in bsf]

    idx = 0
    t_idx = 0
    s_offsets = []
    t_offsets = []
    if text:
        for s in text.split("\n"):
            s_offsets.append([idx, idx + len(s)])
            for t in s.strip().split(" "):
                t_offsets.append([t_idx, t_idx + len(t)])
                t_idx += len(t) + 1

            idx += len(s) + 1
            t_idx = idx

    ts = int(time.time())
    vulyk = {
        "modifications": [],
        "equivs": [],
        "protocol": 1,
        "ctime": ts,
        "triggers": [],
        "text": text,
        "source_files": ["ann", "txt"],
        "messages": [],
        "sentence_offsets": s_offsets,
        "comments": [],
        "entities": ents,
        "mtime": ts,
        "relations": [],
        "token_offsets": t_offsets,
        "action": "getDocument",
        "normalizations": [],
        "attributes": [],
        "events": [],
        "document": "",
        "collection": "/",
    }

    return vulyk


def convert(args):
    for text in map(pathlib.Path, glob.glob(args.text_files)):
        log.info(f"Found text file {text}, parsing it")

        markup = ""

        if not args.ignore_annotations:
            if args.ann_autodiscovery == "append":
                ann = text.with_name(text.name + ".ann")
            else:
                ann = text.with_suffix(".ann")

            if not ann.exists():
                log.warning(f"Cannot find annotation file {ann} alongside to text file {text}, skipping")
            else:
                markup = ann.read_text()

        vulyk_obj = convert_bsf_2_vulyk(text.read_text(), markup)
        print(json.dumps(vulyk_obj, ensure_ascii=False, sort_keys=True))


def tag(args):
    if args.ner_framework == "stanza":
        model = StanzaNER(args.ner_model)
    elif args.ner_framework == "spacy":
        model = SpacyNER(args.ner_model)

    for text in map(pathlib.Path, glob.glob(args.text_files)):
        log.info(f"Found text file {text}, tagging it")

        token_list = tokenize_text(text.read_text())

        # we have list<paragraphs> of list<sentences> of list<tokens>
        paragraph = ["\n".join([" ".join(t) for t in sent]) for sent in token_list]
        txt = "\n".join(paragraph)  # stanza bug does not allow for double new line symbol right now

        markup = model.tag_text(txt)

        vulyk_obj = convert_bsf_2_vulyk(txt, markup)

        print(json.dumps(vulyk_obj, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    logging.basicConfig()

    parser = argparse.ArgumentParser(
        description="Convert tokenized pre-annotated text or tag generic text to json file supported by Vulyk. "
        "Data file can be supplied via cmd line arguments "
        "or you can pipe data in and out of this script like:"
        "`cat file.txt | python3 convert2vulyk.py tag >> save_to_file.json`"
    )

    parser.add_argument(
        "text_files",
        help="File mask to collect text files to process."
        " Must be tokenized if convert command is used. "
        "*.ann for lang-uk data set",
    )

    parser.add_argument(
        "-d",
        "--debug",
        help="Print even more logs (debug)",
        action="store_const",
        dest="loglevel",
        const=logging.DEBUG,
        default=logging.WARNING,
    )
    parser.add_argument(
        "-v",
        "--verbose",
        help="Print more logs (info)",
        action="store_const",
        dest="loglevel",
        const=logging.INFO,
    )

    subparsers = parser.add_subparsers(help="Available commands")

    convert_parser = subparsers.add_parser(
        "convert",
        help="Convert tokenized texts (with optional annotations in a separate files) to a Vulyk format",
    )

    convert_parser.set_defaults(func=convert)
    convert_parser.add_argument(
        "--ann_autodiscovery",
        default="replace",
        choices=("append", "replace"),
        help="How to find *.ann files: by appending or replacing the extension",
    )
    convert_parser.add_argument(
        "--ignore_annotations", default=False, action="store_true", help="Do not try to load *.ann files"
    )

    tag_parser = subparsers.add_parser("tag", help="Tag given files using one of frameworks/models specified in params")

    tag_parser.add_argument(
        "--ner_framework",
        choices=("stanza", "spacy"),
        default="stanza",
        help="Which framework to use for the tagging",
    )

    tag_parser.add_argument(
        "--ner_model",
        default="uk",
        help="Which model to use. Stanza has pre-built model `uk` for ukrainian language. "
        "For Spacy you might specify pre-built model (you should run `python -m spacy download model_name` first) "
        "or provide a path to the directory with the model",
    )

    tag_parser.set_defaults(func=tag)

    args = parser.parse_args()

    log.setLevel(args.loglevel)

    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_usage()
