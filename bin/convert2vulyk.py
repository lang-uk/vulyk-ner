#!env python

import argparse
import json
import logging
import re
import time
import glob
import pathlib
from typing import Any, Generator
from tokenize_uk import tokenize_text  # type: ignore
from collections import namedtuple

log = logging.getLogger(__name__)

BsfInfo = namedtuple("BsfInfo", "id, tag, start_idx, end_idx, token")


class AbstractNER:
    def __init__(self, model: str) -> None:
        raise NotImplementedError()

    def tag_text(self, txt: str) -> str:
        raise NotImplementedError()


class StanzaNER(AbstractNER):
    def __init__(self, model: str) -> None:
        import stanza  # type: ignore

        logging.getLogger("stanza").setLevel(log.level)
        stanza.download(model)

        self.ner = stanza.Pipeline(lang=model, processors="tokenize,mwt,ner", tokenize_pretokenized="true")

    def tag_text(self, txt: str) -> str:
        doc = self.ner(txt)

        brat_str: str = ""

        for tok_i, ent in enumerate(doc.ents):
            brat_str += f"T{tok_i + 1}\t{ent.type} {ent.start_char} {ent.end_char}\t{ent.text}\n"

        return brat_str


class SpacyNER(AbstractNER):
    def __init__(self, model: str) -> None:
        import spacy

        self.ner = spacy.load(model)

    def tag_text(self, txt: str) -> str:
        doc = self.ner(txt)

        brat_str: str = ""

        if doc.ents:
            for tok_i, ent in enumerate(doc.ents):
                brat_str += f"T{tok_i + 1}\t{ent.label_} {ent.start_char} {ent.end_char}\t{ent.text}\n"

        return brat_str


def parse_bsf(bsf_data: str) -> list[BsfInfo]:
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
    result: list = []
    for m in ln_ptrn.finditer(data):
        bsf = BsfInfo(m.group(1), m.group(2), int(m.group(3)), int(m.group(4)), m.group(5).strip())
        result.append(bsf)
    return result


def simple_tokenizer(text: str) -> list[list[str]]:
    """
    Given whitespace/newline tokenized text, return the
    list of sentences (where each sentence is made of tokens)
    using whitespaces and newlines
    """

    doc: list[list[str]] = []
    if text:
        for s in text.split("\n"):
            doc.append(s.strip().split(" "))

    return doc


def reconstruct_tokenized(tokenized_text: list[list[str]]) -> Generator[str, None, None]:
    SPACES_BEFORE: str = "([“«"
    NO_SPACE_BEFORE: str = ".,:!?)]”»"

    for s_idx, s in enumerate(tokenized_text):
        if s_idx > 0:
            yield "\n"
        prev_token = ""
        for w_idx, w in enumerate(map(str.strip, s)):
            if not w:
                continue

            if w_idx > 0 and w not in NO_SPACE_BEFORE and not prev_token in SPACES_BEFORE:
                yield " "

            yield w
            prev_token = w


def convert_bsf_2_vulyk(tokenized_text: list[list[str]], bsf_markup: str) -> dict:
    """
    Given tokenized text and named entities in Brat standoff format, generate object
    in the format compatible with Vulyk markup tool.
    :param text: tokenized text (space as separator)
    :param bsf_markup: named entities in Brat standoff format
    :return: dict that can be directly converted to Vulyk json file
    """

    tags_mapping = {"PERS": "ПЕРС", "ORG": "ОРГ", "LOC": "ЛОК", "MISC": "РІЗН"}

    bsf: list[BsfInfo] = parse_bsf(bsf_markup)
    ents: list[list[Any]] = [[e.id, tags_mapping.get(e.tag, e.tag), [(e.start_idx, e.end_idx)]] for e in bsf]

    idx: int = 0
    t_idx: int = 0
    s_offsets: list[tuple[int, int]] = []
    t_offsets: list[tuple[int, int]] = []
    text: str = ""
    s: str = ""

    for w in reconstruct_tokenized(tokenized_text):
        if w == "\n":
            if s:
                s_offsets.append((idx, idx + len(s)))

            idx += len(s) + 1
            s = ""
        else:
            s += w

        text += w

        if w not in [" ", "\n"]:
            t_offsets.append((t_idx, t_idx + len(w)))

        t_idx += len(w)

    if s:
        s_offsets.append((idx, idx + len(s)))

    ts: int = int(time.time())
    vulyk: dict = {
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


def convert(text_files: str, ignore_annotations: bool, ann_autodiscovery: str) -> None:
    for text in map(pathlib.Path, glob.glob(text_files)):
        log.info(f"Found text file {text}, parsing it")

        markup = ""

        if not ignore_annotations:
            if ann_autodiscovery == "append":
                ann = text.with_name(text.name + ".ann")
            else:
                ann = text.with_suffix(".ann")

            if not ann.exists():
                log.warning(f"Cannot find annotation file {ann} alongside to text file {text}, skipping")
            else:
                markup = ann.read_text()

        vulyk_obj = convert_bsf_2_vulyk(text.read_text(), markup)
        print(json.dumps(vulyk_obj, ensure_ascii=False, sort_keys=True))


def convert_command(args: argparse.Namespace) -> None:
    return convert(
        text_files=args.text_files,
        ignore_annotations=args.ignore_annotations,
        ann_autodiscovery=args.ann_autodiscovery,
    )


def tag(text_files: str, ner_framework: str, ner_model: str) -> None:
    if ner_framework == "stanza":
        model: AbstractNER = StanzaNER(ner_model)
    elif ner_framework == "spacy":
        model = SpacyNER(ner_model)

    for text in map(pathlib.Path, glob.glob(text_files)):
        log.info(f"Found text file {text}, tagging it")

        token_list = tokenize_text(text.read_text())

        # we have list<paragraphs> of list<sentences> of list<tokens>
        paragraph = ["\n".join([" ".join(t) for t in sent]) for sent in token_list]
        txt = "\n".join(paragraph)  # stanza bug does not allow for double new line symbol right now

        markup = model.tag_text(txt)

        vulyk_obj = convert_bsf_2_vulyk(txt, markup)

        print(json.dumps(vulyk_obj, ensure_ascii=False, sort_keys=True))


def tag_command(args: argparse.Namespace) -> None:
    return tag(args.text_files, args.ner_framework, args.ner_model)


if __name__ == "__main__":
    logging.basicConfig()

    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description="Convert tokenized pre-annotated texts or tag generic texts to jsonlines file supported by Vulyk. \n"
        "Data files supplied via glob-like cmd line arguments. Output goes directly to stdout. \n"
        "Script has two modes: convert, to convert texts (with optional annotations) "
        "and tag, to tag provided tokenized texts using one of supported frameworks. "
        "Please check help texts for the respecting commands for details on parameters."
    )

    subparsers: argparse._SubParsersAction = parser.add_subparsers(dest="cmd", help="Available commands")

    convert_parser: argparse.ArgumentParser = subparsers.add_parser(
        "convert",
        help="Convert tokenized texts (with optional annotations in a separate files) to a Vulyk format "
        "To make it parse all text files together with annotations you should use something like this "
        "`python bin/convert2vulyk.py convert -v 'corpus/*.txt'`. Annotation auto-discovery is ruled "
        "by the setting --ann_autodiscovery, which might append or replace .ann extension in the name of the text file "
        "To disable annotation auto-discovery use --ignore_annotations flag",
    )

    convert_parser.set_defaults(func=convert_command)
    convert_parser.add_argument(
        "--ann_autodiscovery",
        default="replace",
        choices=("append", "replace"),
        help="How to find *.ann files: by appending or replacing the extension",
    )
    convert_parser.add_argument(
        "--ignore_annotations", default=False, action="store_true", help="Do not try to load *.ann files"
    )

    tag_parser: argparse.ArgumentParser = subparsers.add_parser(
        "tag",
        help="Tag given files using one of frameworks/models specified in params. "
        "Currently the script supports Stanza and Spacy frameworks. To use the script in this mode you should install "
        "additional packages from extra_requirements.txt. "
        "Make sure that you have enough RAM and some patience",
    )

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

    tag_parser.set_defaults(func=tag_command)

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

    args: argparse.Namespace = parser.parse_args()

    log.setLevel(args.loglevel)

    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_usage()
